"""
.. module:: cdp_identification

cdp_identification
*************

:Description: cdp_identification

    Port to python of the matlab code for CDP identification

:Authors: bejar
    

:Version: 

:Created on: 30/06/2015 15:19 

"""

__author__ = 'bejar'

import numpy as np
from config.experiments import experiments, lexperiments
import scipy.io
from util.plots import show_signal
import time

def uniquetol(peaks, tol):
    """
    returns the list of the indices of the peaks that are at a distance less than the tolerance to the
    previous peaks

    The list of peaks is a triple, the time of the peak is the first element

    :param v:
    :param tol:
    :return:
    """

    lres = []
    curr = peaks[0]
    lres.append(0)
    for i in range(1,peaks.shape[0]):
        if peaks[i] - curr > tol:
            curr = peaks[i]
            lres.append(i)
    return lres


def integIneqG(data,QI1,QI2,QF1,QF2):
    """
    Pseudo peak test, compares the sum of the bins of the data to check if
    it has a peaky shape

    It should be generalize to any number of bins, currently only 7 bins are possible

    :return:
    """
    bins=7
    #bins=8;

    dataLength = len(data)

    minval = np.min(data)
    maxval = np.max(data)

    normData = (data - minval) / (maxval - minval)

    binLength = dataLength / bins

    integData= np.zeros(bins)
    for i in range(bins):
        integData[i] = np.sum(normData[i*binLength:(i+1)*binLength])

    sumData = np.sum(integData)

    quotI1 = integData[2]/sumData
    quotI2 = (integData[2]+integData[3])/sumData
    quotF1 = integData[7]/sumData
    quotF2 = (integData[6]+integData[7])/sumData

    intTest = (integData[2]+integData[3]<integData[4]+integData[5]) and \
              (integData[3]<integData[4]) and \
              (integData[5]+integData[6]) and \
              (integData[6]+integData[7]<integData[4]+integData[5]) and \
              (quotI1<QI1) and (quotI2<QI2) and (quotF1<QF1) and (quotF2<QF2)

    return intTest


def nextpow2(n):
    """
    Computes the next power of 2 of a number
    :param n:
    :return:
    """
    m_f = np.log2(n)
    m_i = np.ceil(m_f)
    return 2**m_i


def fifft(t, peak, low_cutoff=0, high_cutoff=0, tap=0, myfreq=None):
    """
    Returns the peaks with filtered frequencies

    Based on the original Matlab code

    Tappering disabled for now

    :param t:
    :param peak:
    :param par:
    :return:
    """

    Fs = 1/(t[1]-t[0])
    N = len(peak)

    Nfft = nextpow2(N)

    if low_cutoff < 0:
        low_cutoff = 0
    if high_cutoff == 0:
        high_cutoff = Fs

    f = Fs/2*np.linspace(0,1,1+Nfft/2)  # create freqs vector
    xo = np.zeros(Nfft)
    dw = np.floor((Nfft-N)/2)
    xo[dw:N+dw] = peak
    peak = xo  # add zeros before and aftermx

    #if (tap)  H=sigwin.tukeywin(Nfft,tap); win=generate(H)';    x=x.*win; end

    y = np.fft.fft(peak)/N  # perform fft transform

    # filter amplitudes (deletes the aplitudes outside the cutoff ranges)
    y2 = ffft(f, y, low_cutoff, high_cutoff, myfreq)
    #print y2
    X = np.real(np.fft.ifft(y2))
    X = X[dw:N+dw-1]*N
    return X, f, y, y2


def ffft(f, y, low_cutoff, high_cutoff, wins=None):
    """
    Suposedly deletes the amplitudes of the fft that are outside the cutoffs so
    the inverse FFT returns the smoothed peak

    :param f:
    :param y:
    :param par1:
    :param par2:
    :param myfreq:
    :return:
    """
    nf = len(f)
    ny = len(y)
    if ((ny/2)+1) != nf:
        print 'unexpected dimensions of input vectors!'
        y2 = -1
        return

    y2 = np.zeros(ny, dtype=np.complex) #y.copy()*0
    # cutoff filter, computes the indices of the frequencies among the cutoffs
    if high_cutoff is not None or low_cutoff is not None:
        ind1 = f <= high_cutoff
        ind2 = f >= low_cutoff
        #print np.sum(ind1), np.sum(ind2)
        ind3 = np.logical_and(ind2,ind1)
        y2[ind3] = y[ind3]  # insert required elements
    else:
        y2 = y

    #print y2[0:20]

    # dominant freqs filter
    # I dont know what this actually does
    if wins is not None:
         temp = abs(y2[0:nf-1])
         y2 = np.zeros(ny)
         for k in range(wins):   # number of freqs that I want
              tmaxi = np.argmax(temp)
              y2[tmaxi] = y[tmaxi] # insert required element
              temp[tmaxi] = 0 # eliminate candidate from list

    # create a conjugate symmetric vector of amplitudes
    for k in range(nf+1, ny):
        y2[k] = np.conj(y2[((ny-k+1) % ny)+1])

    return y2

def smot(t, x, ifreq, ffreq, tapering, fft_freq, ismot):
    """
    Original matlab code used ismot to select the smoothing method
    using only fft for now

    :param t:
    :param xs:
    :param par:
    :param ismot:
    :return:
    """
    return fifft(t, x, ifreq, ffreq, tapering, fft_freq)


def cdp_identification(X, T, Fs):
    """

    :param X: Time series data
    :param T: Window length
    :param Fs: Sampling
    :return:
    """

    ifreq = 0.0   # Frequency cutoff low
    ffreq = 70.0  # Frequency cutoff high

    tapering = 0.0 # tapering window use tukey window tap=0 no window, tap=1 max tapering
    fft_freq = None  # max number of freqs used in FFT

    upthreshold = 1        # Outliers threshold *** ADDED by Javier
    downthreshold = -0.4   # Outliers threshold *** ADDED by Javier

    threshold = 0.05        # Peaks Max-Min in window above threshold in amplitude
    peakprecision = T/12     # Peaks localization time resolution in points
    RCoinc = T/6             # Peak synchronization radius
    Tpk = T/4                # Quality filter time window subdivision
    qualc = True             # apply quality cut, =0 do not apply quality cut
    factp = 1.5              # Quality cut on Peaks in windows
    factm = 1.5              # Pv=max(FFT(signal)) Dm=mean(FFT(signal before Pv)(1:Tpk))
                             # Dp=mean(FFT(signal after Pv))(Tw-Tpk:Tw)
                             # quality cut:  Pv>factm*Dm&&Pv>factp*Dp
    quot = [0.19, 0.36, 0.23, 0.36] # Integration test parameters
    testsn = True # =1 apply signal to noise ratio quality cut =0 do not apply this quality cut

    forceTm = 10             #=0 smart peak search =Tm force fixed Tm step peak search
    forcedT = 1              # percentage of the data to be processed

    freq = fft_freq
    if freq == 0:
        freq = None
    ismot = 2          #=1 or 2 use FFT to smooth signal, =3 use wavelet to smooth signal

    #Peaks location in time window =Tw/npz
    npz = 2     # centered peak

    Nmxx, Nsig = X.shape

    Nmax = np.floor(forcedT*Nmxx) # Max numner of points in file
    Tmax = Nmax/Fs               # Time max analyzed in sec
    Tw = int(2 * np.round(T*Fs/2))    # Number of points in window (Tw must be an even number)
    t = np.array(range(Tw))/Fs             # Time axis in window
    Tpk = np.floor(Tpk*Fs)
    peakprecision = np.floor(peakprecision*Fs)


    ipeakM = [] # This list contains the index of the center of the peak, the Sum and the RMS
    SNp = []
    RMSp = []
    Tm = 1
    for j in [0]: #range(Nsig):   #Loop over different sensors
        print 'Peaks identification: analyzing sensor N ', j, time.ctime()
        tstop = 0
        tstart = 1
        ipeakMj = []
        SNpj = []
        RMSpj = []
        while tstop < Nmax:
            tstop = min(Nmax,tstart + Tw - 1)
            xs = X[tstart:tstop, j]
            Nl = len(xs)
            if Nl < Tw:
                xs = np.hstack((xs, np.zeros(Tw-Nl)))

            xf, f, y, y2 = smot(t, xs, ifreq, ffreq, tapering, fft_freq, ismot)  # signal smooth in frequency interval
            xf -= np.min(xf)
            qpeak = (np.max(xf) > threshold) and (np.max(xf) < upthreshold) and (np.min(xf) > downthreshold) # *** up/downthreshold ADDED by Javier

            #Peaks second level cuts we only consider time windows
            #with centered peaks and minimum peaks amplitude >threshold
            Tm = np.argmax(xf[np.floor(Tw/npz)+2:Tw])+1 #smart peaks search
            if qpeak:   #store the time window only if there is a peak
                #Nw = Tw - (2 * np.floor(peakprecision/4))  #length(miv);
                Pv = np.max(xf[np.floor(peakprecision/4):Tw-np.floor(peakprecision/4)])
                indp = np.argmax(xf[np.floor(peakprecision/4):Tw-np.floor(peakprecision/4)])
                Pkv = np.max(xf[np.floor(Tw/npz)-peakprecision:np.floor(Tw/npz)+peakprecision])
                Tcentr = (Pv == Pkv)


                #evaluate quality of the peak
                Tqpeak = True
                #Tqint = True
                if qualc:
                    Dp = 1
                    if Tpk > 0:
                        Dp = abs(np.mean(xf[0:Tpk]))

                    Dm =1
                    if Tpk > 0:
                        Dm = abs(np.mean(xf[Tw-Tpk:Tw]))
                    Tqpeak = (Pv > factp*Dp) and (Pv > factm*Dm)

                    #Tqint = integIneqG(xf,quot)

                # check the peak
                quality = Tcentr and Tqpeak
                if quality:
                    # Store the index of the peak, sum ratio and RMS
                    print '-->', tstart+np.floor(peakprecision/4)+indp
                    ipeakMj.append(tstart+np.floor(peakprecision/4)+indp)
                    SNpj.append(np.sum(y2*np.conj(y2))/sum(y*np.conj(y)))
                    RMSpj.append(np.std(xs))
                    #print tstart+np.floor(peakprecision/4)+indp
                    # store time of max peak in window
                    Tm = int(np.floor(Tw/npz)+1)
                    #show_signal(xf)

                # check which peaks are we throwing away
                # noquality=Tcentr and not Tqpeak
                # if noquality:
                #     ipeakMnoQj.append(tstart+np.floor(peakprecision/4)+indp)

            # if forceTm == 0:
            #     Tm = forceTm  # force exhaustive peaks search
            tstart += Tm
            #print Tm
        # Add the peaks of the signal to the datastructure
        ipeakM.append(np.array(ipeakMj))
        SNp.append(np.array(SNpj))
        RMSp.append(np.array(RMSpj))

    print 'Filtering near peaks', time.ctime()
    # This eliminates all the peaks that are at a distance less than the peak precision parameter
    # TODO: Change the previous part so this is not necessary
    ipeakMsel = []
    SNpsel = []
    RMSpsel = []
    for peaks,sn,rms in zip(ipeakM, SNp, RMSp):
        lind = uniquetol(peaks, peakprecision)
        ipeakMsel.append(peaks[lind])
        SNpsel.append(sn[lind])
        RMSpsel.append(rms[lind])


    # Signal to noise ratio filtering
    signal_noise_tolerance = 1.4 # Tolerance for Signal/Noise ratio
    co = 0.96  # parameters used in SNp selection cut thdPP=co*(1-ao*exp(-so*RMSp(i,j)))/(1-bo*exp(-so*RMSp(i,j)));
    ao = 2
    bo = 1
    so = 50
    ko = 6.41

    for peaks in ipeakMsel:
        print len(peaks)
    print 'Filtering Noise Ratio Peaks ', time.ctime()

    ipeakM = []
    for i, peaks in enumerate(ipeakMsel):
        #thdP = np.mean(SNpsel[i]) - signal_noise_tolerance * np.std(SNpsel[i])
        #thdR = np.mean(RMSpsel[i]) + ko * np.std(RMSpsel[j])
        ipeakMj = []
        for j in range(peaks.shape[0]):
            tcenter = peaks[j]
            tstart = np.max([1,tcenter - np.floor(Tw / npz)])
            tstop = np.min([Nmax, tstart + Tw - 1])
            tmp = X[tstart:tstop, i]

            Nl = len(tmp)
            if Nl < Tw:
                tmp = np.hstack((tmp, np.zeros(Tw-Nl)))

            #PeakM(i,:,j)=tmp; # select the signal
            thdPP = co*(1-ao*np.exp(-so*RMSpsel[i][j]))/(1-bo*np.exp(-so*RMSpsel[i][j]))
            if  SNpsel[i][j]>thdPP:
                ipeakMj.append(peaks[j])
        ipeakM.append(ipeakMj)

    print 'The end ', time.ctime()

    for peaks in ipeakM:
        print len(peaks)


# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
    #lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

    #lexperiments = ['e130827', 'e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['130827']


    datasufix = ''#'-RawResampled'

    wtime = 120e-3 # Window length in miliseconds

    for expname in lexperiments:
        datainfo = experiments[expname]
        sampling = datainfo.sampling #/ 6.0

        for dfile in [datainfo.datafiles[0]]:

            print datainfo.dpath + dfile + '.mat'
            mattime = scipy.io.loadmat(datainfo.dpath + dfile + '.mat')
            raw = mattime['data']

            cdp_identification(raw,  wtime, datainfo.sampling)

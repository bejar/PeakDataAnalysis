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
from util.plots import show_signal, show_two_signals
import time
import h5py
import pyfftw


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



def fifft(Nfft, fmask, peak, dw, N):
    """
    Returns the peaks with filtered frequencies

    Based on the original Matlab code

    Tappering disabled for now

    :param t:
    :param peak:
    :param par:
    :return:
    """


    xo = np.zeros(Nfft)
    xo[dw:N+dw] = peak

    y = np.fft.rfft(xo)/N  # perform fft transform

    # filter amplitudes (deletes the aplitudes outside the cutoff ranges)
    y2 = ffft(fmask, y)

    X = np.fft.irfft(y2)
    X = X[dw:N+dw-1]*N
    return X, y, y2


def ffft(fmask, y):
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
    nf = len(fmask)
    ny = len(y)

    y2 = np.zeros(ny, dtype=np.complex)
    # cutoff filter, computes the indices of the frequencies among the cutoffs
    if fmask is not None:
        y2[fmask] = y[fmask]  # insert required elements
    else:
        y2 = y

    # create a conjugate symmetric vector of amplitudes
    for k in range(nf+1, ny):
        y2[k] = np.conj(y2[((ny-k) % ny)])
    return y2


def cdp_identification(X, T, Fs):
    """

    :param X: Time series data
    :param T: Window length
    :param Fs: Sampling
    :return:
    """

    ifreq = 0.0   # Frequency cutoff low
    ffreq = 70.0  # Frequency cutoff high

    tapering = 0.0  # tapering window use tukey window tap=0 no window, tap=1 max tapering
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

    Nfft = int(2**np.ceil(np.log2(Tw)))

    f = Fs/2*np.linspace(0, 1, 1 + Nfft / 2)  # create freqs vector

    if ifreq is not None or ffreq is not None:
        ind1 = f <= ffreq
        ind2 = f >= ifreq
        fmask = np.logical_and(ind2,ind1)

    Tpk = int(np.floor(Tpk*Fs))
    peakprecision = np.floor(peakprecision*Fs)

    ipeakM = [] # This list contains the index of the center of the peak, the Sum and the RMS
    SNp = []
    RMSp = []
    Tm = 1
    dw = np.floor((Nfft-Tw)/2)
    for j in range(Nsig):   #Loop over different sensors
        print 'Peaks identification: analyzing sensor N ', j, time.ctime()
        tstop = 0
        tstart = 1
        ipeakMj = []
        SNpj = []
        RMSpj = []
        nt = 0
        while tstop < Nmax:
            tstop = min(Nmax,tstart + Tw - 1)
            xs = X[tstart:tstop, j]
            Nl = len(xs)
            if Nl < Tw:
                xs = np.hstack((xs, np.zeros(Tw-Nl)))

            xf, y, y2 = fifft(Nfft, fmask, xs, dw, Tw)  # signal smooth in frequency interval

            xf -= np.min(xf)
            qpeak = (np.max(xf) > threshold) and (np.max(xf) < upthreshold) and (np.min(xf) > downthreshold) # *** up/downthreshold ADDED by Javier

            #Peaks second level cuts we only consider time windows
            #with centered peaks and minimum peaks amplitude >threshold
            Tm = np.argmax(xf[np.floor(Tw/npz)+2:Tw])+1 #smart peaks search
            if qpeak:   #store the time window only if there is a peak
                Pv = np.max(xf[np.floor(peakprecision/4):Tw-np.floor(peakprecision/4)])
                indp = np.argmax(xf[np.floor(peakprecision/4):Tw-np.floor(peakprecision/4)])
                Pkv = np.max(xf[np.floor(Tw/npz)-peakprecision:np.floor(Tw/npz)+peakprecision])

                if (Pv == Pkv):
                    #evaluate quality of the peak
                    Tqpeak = False
                    if qualc:
                        Dp = 1
                        if Tpk > 0:
                            Dp = abs(np.mean(xf[0:Tpk]))

                        Dm =1
                        if Tpk > 0:
                            Dm = abs(np.mean(xf[Tw-Tpk:Tw]))
                        Tqpeak = (Pv > (factp*Dp)) and (Pv > (factm*Dm))

                        #Tqint = integIneqG(xf,quot)

                    # check the peak
                    if Tqpeak:
                        # Store the index of the peak, sum ratio and RMS
                        ipeakMj.append(tstart+np.floor(peakprecision/4)+indp)
                        SNpj.append(np.sum(y2*np.conj(y2))/np.sum(y*np.conj(y)))
                        RMSpj.append(np.std(xs))
                        # store time of max peak in window
                        Tm = int(np.floor(Tw/npz)+1)

                # check which peaks are we throwing away
                # noquality=Tcentr and not Tqpeak
                # if noquality:
                #     ipeakMnoQj.append(tstart+np.floor(peakprecision/4)+indp)

            if forceTm != 0:
                 Tm = forceTm  # force exhaustive peaks search
            tstart += Tm
            nt += 1

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

    for peaks in ipeakMsel:
        print len(peaks)

    # Signal to noise ratio filtering
    signal_noise_tolerance = 1.4 # Tolerance for Signal/Noise ratio
    co = 0.96  # parameters used in SNp selection cut thdPP=co*(1-ao*exp(-so*RMSp(i,j)))/(1-bo*exp(-so*RMSp(i,j)));
    ao = 2
    bo = 1
    so = 50
    ko = 6.41

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

    return ipeakM

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
        # f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
        wfile = open(datainfo.dpath + 'peaks-' + expname + '.csv', 'w')

        for dfile in datainfo.datafiles:
            wfile.write(dfile)
            wfile.write('\n')
            print datainfo.dpath + dfile + '.mat'
            mattime = scipy.io.loadmat(datainfo.dpath + dfile + '.mat')
            raw = mattime['data']

            peaks = cdp_identification(raw,  wtime, datainfo.sampling)

            for pk, s in zip(peaks, datainfo.sensors):
                wfile.write(s + ': '+ str(len(pk))+ '\n')
            wfile.write('\n')

            wfile.flush()
        wfile.close()
            # d = f[dfile + '/' + 'L4ci' + '/' + 'Time']
            # dataf = d[()]
            #
            # pk = peaks[0]
            #
            # i = 0
            # j = 0
            # tol = 30
            # print dataf.shape
            # while i < len(pk) and j < dataf.shape[0]:
            #     if abs(pk[i]-dataf[j]) > tol:
            #         if pk[i] < dataf[j]:
            #             print 'Py: ', pk[i]
            #             i += 1
            #         else:
            #             print 'Ml: ', dataf[i]
            #             j += 1
            #     else:
            #         i += 1
            #         j += 1
            #
            # print i, len(pk), j, dataf.shape[0]


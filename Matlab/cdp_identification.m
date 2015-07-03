function cdp_identification(datain,dataout,T,Fs)

%to use the function provide:
%T=time window duration in sec (default T=100e-3)
%Fs=sampling frecuency in Hz (default Fs=1670 Hz)
%datain= input matlab file with data organized as a matrix data(Nmxx,Nsig)
%dataout= output matlab file providing original experiment dataset matrix
%data,  detected peaks for each sensor matrix ipeakM(Npeaks,Nsig) and
%relative peak signal PeakM(Npeaks,Tw,Nsig)


%Peaks reference time window parameters
if nargin<4 Fs=1670; end; %Fs=1670 Hz Sampling reference frequency 
if nargin<3 T=100e-3; end; %T=100e-3sec  Tw=168 points - Time windows 


%selection parameters change if needed
par(1)=0.;       % cutof1 frecuency Low cutoff
par(2)=70;       % cutof2 frecuency High cutoff
par(3)=0;      % tapering window use tukey window tap=0 no window, tap=1 max tapering
par(4)=0;        % max number of freqs used in FFT

%Peaks definition and selection
upthreshold = 1;        % Outliers threshold *** ADDED by Javier
downthreshold = -0.4;    % Outliers threshold *** ADDED by Javier
threshold=0.05;        % Peaks Max-Min in window above threshold in amplitude
peakprecision=T/12;    % Peaks localization time resolution in points
RCoinc=T/6;              % Peak synchronization radius
Tpk=T/4;               % Quality filter time window subdivision
qualc=1;               %=1 apply quality cut, =0 do not apply quality cut
factp=1.5;             % Quality cut on Peaks in windows 
factm=1.5;             % Pv=max(FFT(signal)) Dm=mean(FFT(signal before Pv)(1:Tpk)) 
                       % Dp=mean(FFT(signal after Pv))(Tw-Tpk:Tw)
                       % quality cut:  Pv>factm*Dm&&Pv>factp*Dp 
quot=[0.19, 0.36, 0.23, 0.36];% Integration test parameters
testsn=1; %=1 apply signal to noise ratio quality cut =0 do not apply this quality cut
nsig=1.4; %nsig=1.2; %nsig=1.5; % SNp> mean(SNp)-nsig*std(SNp)
co=0.96;ao=2;bo=1;so=50; ko=6.41; %parameters used in SNp selection cut thdPP=co*(1-ao*exp(-so*RMSp(i,j)))/(1-bo*exp(-so*RMSp(i,j)));

forceTm=10;            %=0 smart peak search =Tm force fixed Tm step peak search 
forcedT=1;             % percentage % of the data to be processed


cutof1=par(1);       cutof2=par(2);     tap=par(3); freq=par(4); if freq==0; freq=[]; end
ismot=2;         %=1 or 2 use FFT to smooth signal, =3 use wavelet to smooth signal

%Peaks location in time window =Tw/npz
npz=2;     % centered peak

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('\n --------------  LOADING EXPERIMENT DATASETS --------- \n');

load(datain);      
[Nmxx, Nsig]=size(data);

Nmax=floor(forcedT*Nmxx); % Max numner of points in file
Tmax=Nmax/Fs;          % Time max analyzed in sec
Tw=2.*round(T*Fs/2);   % Number of points in window (Tw must be an even number)
t=(1:Tw)/Fs;           % Time axis in window
Tpk=floor(Tpk*Fs);
RCoinc=floor(RCoinc*Fs);
peakprecision=floor(peakprecision*Fs);
xmin=0; xmax=Tw; ymax=max(max(data)); ymin=min(min(data)); % reference limits to plot peaks in window

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%preliminary tests  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fprintf('Number of sensors %i \n',Nsig);
fprintf('Time to analyze %6.1f sec \n',Tmax);
fprintf('Sampling frecuency %4.1f Hz \n',Fs);

fprintf('Peaks time window %3.1f msec (%i points)\n',T*1e3,Tw);
cutoff2=cutof2; if cutof2==0 cutoff2=Fs; end
fprintf('Peaks FFT frecuency interval [%2.2f,%2.2f] Hz \n',cutof1,cutoff2);
fprintf('Peaks tapering %1.1f and num frequency %i \n',tap,freq);
fprintf('Peaks precision %i and time window subdivision %i \n',peakprecision,Tpk);
fprintf('Peaks cuts factors factp=%f factpm=%f threshold=%f upthreshold=%f dowthreshold=%f\n ',factp,factm,threshold, upthreshold, downthreshold);
fprintf('Peaks integral cuts factors %f %f %f %f \n',quot(1),quot(2),quot(3),quot(4));


fprintf('\n ----------------  PEAKS IDENTIFICATION --------- \n');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Start peaks selection 
ipeakNo=[]; ipeakM=[];ff=0;
for j=1:1%Nsig  %Loop over different sensors
fprintf('Peaks identification: analyzing sensor N %i \n',j);

Nwin(j)=0;
k=0; r=0; qk=0; tstop=0; tstart=1;
while (tstop<Nmax)         
    Nwin(j)=Nwin(j)+1;
    tstop=min(Nmax,tstart+Tw-1);    
    xs=data(tstart:tstop,j); Nl=length(xs); if (Nl<Tw) xs=[xs ; zeros(Tw-Nl,1)]; end 
    [xf, f, y, y2]=smot(t,xs',par,ismot); %signal smooth in frequency interval
    xf=xf-min(xf);
    qpeak=max(xf)>threshold & max(xf)<upthreshold & min(xf) > downthreshold; % *** up/downthreshold ADDED by Javier
    
    
    %Peaks second level cuts we only consider time windows
    %with centered peaks and minimum peaks amplitude >threshold           
    [Vm Tm]=max(xf(floor(Tw/npz)+2:Tw));    %smart peaks search
        
    if(qpeak)   %store the time window only if there is a peak          
          miv=floor(peakprecision/4):Tw-floor(peakprecision/4);
          Nw=length(miv);
          [Pv indp]=max(xf(miv));  
          Tcentrg=abs(indp-floor(Nw/npz))<=peakprecision;      
          mid=floor(Tw/npz)-peakprecision:floor(Tw/npz)+peakprecision;
          Pkv=max(xf(mid)); 
          Tcentr=(Pv==Pkv);
          
         %evaluate quality of the peak 
          Tqpeak=1;  Tqint=1;
          if qualc
           tdp=1:Tpk;            
           Dp=1; if ~isempty(tdp) [Dp]= abs(mean(xf(tdp))); end          
           tdm=Tw-Tpk:Tw;                         
           Dm=1; if ~isempty(tdm) [Dm]= abs(mean(xf(tdm)));  end                   
           Tqpeak=(Pv>factp*Dp&&Pv>factm*Dm);        
           Tqint=integIneqG(xf,quot(1),quot(2),quot(3),quot(4));           
           %Tqpeak=Tqpeak&&Tqint;
          end

          %fprintf('%d, %d, %f, %f, %f, %f, %f, %f \n', tstart, tstart+floor(peakprecision/4)+indp, Pv, Pkv, Dp, Dm, peakprecision/4, indp);
          %check the peak
           quality=Tcentr&&Tqpeak;
            if quality 
              k=k+1;
              fprintf('Peak %f \n',tstart+floor(peakprecision/4)+indp);
              ipeakM(k,j)=tstart+floor(peakprecision/4)+indp;
              SNp(k,j)=sum(y2.*conj(y2))/sum(y.*conj(y));
              RMSp(k,j)=std(xs);
              
              % store time of max peak in window              
              Tm=floor(Tw/npz)+1;         
            end

            %check which peaks are we throwing away
            noquality=Tcentr&&~Tqpeak;            
            if noquality 
              qk=qk+1;
              ipeakMnoQ(qk,j)=tstart+floor(peakprecision/4)+indp;
            end            
            
    end          
    if forceTm  
      Tm=forceTm;  %force exhaustive peaks search 
    end        
    tstart=tstart+Tm;
 end
end


% This eliminates all the peaks that are at a distance less than the peak precision parameter
ipeakM1=ipeakM; clear ipeakM;
SNp1=SNp; clear SNp; RMSp1=RMSp; clear RMSp;
for j=1:1%Nsig
    tmp=uniquetol(ipeakM1(ipeakM1(:,j)>0,j),peakprecision); Npk=length(tmp);
    ipeakM(1:Npk,j)=tmp;
    [a b c]=intersect(ipeakM(1:Npk,j),ipeakM1(ipeakM1(:,j)>0,j));
    SNp(1:Npk,j)=SNp1(c,j); RMSp(1:Npk,j)=RMSp1(c,j);    
end
clear ipeakM1; clear SNp1; clear RMSp1;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%calibrate detected signals with peaks timing
clear Mpset
for j=1:1%Nsig
    thdP(j)=mean(SNp(SNp(:,j)>0,j))-nsig.*std(SNp(SNp(:,j)>0,j));
    thdR(j)=mean(RMSp(RMSp(:,j)>0,j))+ko.*std(RMSp(RMSp(:,j)>0,j));
    Mpset{j}=ipeakM(ipeakM(:,j)>0,j); Mpeak(j)=length(Mpset{j});
    for i=1:Mpeak(j)
     tcenter=Mpset{j}(i);
     tstart=max(1,tcenter-floor(Tw/npz));
     tstop=min(Nmax,tstart+Tw-1); 
     tmp=data(tstart:tstop,j); Nl=length(tmp); if (Nl<Tw) tmp=[tmp ; zeros(Tw-Nl,1)]; end
     PeakM(i,:,j)=tmp; %select the signal
     thdPP=co*(1-ao*exp(-so*RMSp(i,j)))/(1-bo*exp(-so*RMSp(i,j)));
     testSN=SNp(i,j)>thdPP;
     ipeakMS(i,j)=ipeakM(i,j)*testSN;
     if ~testSN ipeakNO(i,j)=ipeakM(i,j); end
    end   
    MpsetS{j}=ipeakMS(ipeakMS(:,j)>0,j); MpeakS(j)=length(MpsetS{j});    
end

%clear peaks with low signal to noise ratio
if testsn 
    Mpseto=Mpset; ipeakMo=ipeakM; 
    Mpset=MpsetS; ipeakM=ipeakMS; 
end


 fprintf('\n');
 for j=1:Nsig
  fprintf('Sensor N %i analyzed time windows %i \n',j,Nwin(j));
 end
 fprintf('\n');    
 for j=1:Nsig
  fprintf('Sensor N %i selected peaks %i \n',j,Mpeak(j));
 end


  

fprintf('Saving selected peaks in data file=%s \n',dataout);

%data original experiment dataset 
%ipeakM(Npeaks,Nsens) (quality cuts) detected peaks for each sensor Nsens 
%PeakM relative peak signal Tw

save(dataout,'data','ipeakM','PeakM');


 
end













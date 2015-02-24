function [X, f, y, y2] = smot(t, x, par,ismot)


if ismot==1
    [X, f, y, y2]=Mfftf2(t,x,par); %FFT
%    [X, f, y, y2]=Mfftf2(t,x,cutofL,cutofH,taper,frequencies,ifig); %FFT
%par(1)=cutofL; par(2)=cutofH; par(3)=taper; par(4)=frequencies;

elseif ismot==2
    [X, f, y, y2]=fifft(t,x,par); %(as 2 but faster)
%    [X, f, y, y2]=Mfftf2(t,x,cutofL,cutofH,taper,frequencies); %FFT
%par(1)=cutofL; par(2)=cutofH; par(3)=taper; par(4)=frequencies;

elseif ismot==3
    [X, f, y, y2]=Mwavelet(t,x,par);  %wavelet
%    [X, f, y, y2]=Mfftf2(t,x,wlev,waven); %DFT
%par(1)=wlev; par(2)=waven;
end


return
end

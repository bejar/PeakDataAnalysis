function [X, f, y, y2]=Mwavelet(t, x, par)

wlev=par(1);
waven=par(2);

% Definitions
Fs=1/(t(2)-t(1)); %sampling freq
N=length(x);
Nfft=2^nextpow2(N);
f=Fs/2*linspace(0,1,1+Nfft/2); % create freqs vector

[C,L] = wavedec(x,wlev,waven);
y=C;
y2 = appcoef(C,L,waven,wlev);
X= wrcoef('a',C,L,waven,wlev); % An
return
end

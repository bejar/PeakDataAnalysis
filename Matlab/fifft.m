function [X, f, y, y2] = fifft(t,x,par)

Lp=length(par);
par1=par(1);
par2=par(2);



tap=0;
if Lp>2,
    tap=par(3);
end

myfreq=[];
if Lp>3,
    myfreq=par(4);
    if myfreq==0 myfreq=[]; end
end

 Fs=1/(t(2)-t(1));  N=length(x); Nfft=2^nextpow2(N);
 if par1<0 par1=0; end
 if par2==0; par2=Fs; end


 f=Fs/2*linspace(0,1,1+Nfft/2); % create freqs vector
 xo=zeros(1,Nfft);  dw=floor((Nfft-N)/2);   xo(dw:N+dw-1)=x;  x=xo; %add zeros before and aftermx

 if (tap)  H=sigwin.tukeywin(Nfft,tap); win=generate(H)';    x=x.*win; end


 y=fft(x,Nfft)/N; % perform fft transform
 y2=ffft(f, y, par1, par2,myfreq); % filter amplitudes
 X=real(ifft(y2));
% X=X(1:N)*N;
X=X(dw:N+dw-1)*N;

return
end

function y2=ffft(f, y, cutoff1, cutoff2,wins)
nf=length(f);
ny=length(y);
if ~(ny/2+1 == nf),
    disp('unexpected dimensions of input vectors!')
    y2=-1;
    return
end

y2=zeros(1,ny);
% cutoff filter
if ~isempty(cutoff2)||~isempty(cutoff1)
    ind1=find(f<=cutoff2);
    ind2=find(f>=cutoff1);
    ind3=intersect(ind2,ind1);
    y2(ind3) = y(ind3); % insert required elements
else
    y2=y;
end


% % dominant freqs filter
 if ~isempty(wins),
     temp=abs(y2(1:nf));
     y2=zeros(1,ny);
     for k=1:wins,   % number of freqs that I want
         [tmax, tmaxi]=max(temp);
         y2(tmaxi) = y(tmaxi); % insert required element
         temp(tmaxi)=0; % eliminate candidate from list
     end
  end


% create a conjugate symmetric vector of amplitudes
for k=nf+1:ny,
    y2(k) = conj(y2(mod(ny-k+1,ny)+1)); % formula from the help of ifft
end
return
end
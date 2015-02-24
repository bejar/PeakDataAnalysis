function [intTest quota]= integIneqG(data,QI1,QI2,QF1,QF2)
% Computes an integration test to the signal to make sure is a proper peak

bins=7;
%bins=8;

dataLength=length(data);

minval= min(data);
maxval=max(data);

normData= (data-minval)/(maxval-minval);

binLength=dataLength/bins;

integData=zeros(bins);
for i= 1:dataLength
  integData((round(i/binLength)+1))=integData((round(i/binLength)+1))+normData(i);
end

sumData=sum(normData);

quotI1= integData(2)/sumData;
quotI2= (integData(2)+integData(3))/sumData;
quotF1= integData(7)/sumData;
quotF2= (integData(6)+integData(7))/sumData;

quota(1)=quotI1;
quota(2)=quotI2;
quota(3)=quotF1;
quota(4)=quotF2;



intTest=(integData(2)+integData(3)<integData(4)+integData(5))&& ...
     (integData(3)<integData(4))&&(integData(5)+integData(6))&& ...
        (integData(6)+integData(7)<integData(4)+integData(5))&& ...
        (quotI1<QI1) && (quotI2<QI2) && (quotF1<QF1) && (quotF2<QF2);

return
end
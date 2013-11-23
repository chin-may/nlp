function [res, idf]  = tf_idf(tdmat)
idf = 1./ log(sum(tdmat>0));
res = tdmat;
for i=1:size(idf,2)
    res(:,i) = res(:,i)*idf(i);
end

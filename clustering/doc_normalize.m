function res  = doc_normalize(tdmat)
res = tdmat';
for i=1:size(res,2)
    res(:,i) = res(:,i)/((res(:,i)')* res(:,i));
end
res = res';

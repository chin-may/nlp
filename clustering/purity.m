function [purity, wt_pur,clas]  = purity(centers, classes)
% For every cluster, purity contains the fraction of the max class in that 
% cluster. wt_pur is the weighted average of purities over data points
% classes contains the majority class of every cluster
wt_pur = 0;
for i=unique(centers)
    locs = find(centers==i);
    labels = classes(locs);
    clas(i) = mode(labels);
    purity(i) = sum(labels==mode(labels))/size(labels,2);
    wt_pur =wt_pur+ purity(i) * size(labels,2);
end

wt_pur = wt_pur / size(centers,2);
purity=purity';

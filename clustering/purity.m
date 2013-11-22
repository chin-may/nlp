function [purity, wt_pur,clas]  = purity(centers, classes)
% centers is a column containing the cluster to which each point is assigned
% classes is a column containing the class to which each point belongs
% For every cluster, purity contains the fraction of the max class in that 
% cluster. wt_pur is the weighted average of purities over data points
% classes contains the majority class of every cluster
wt_pur = 0;
for i=1:size(unique(centers),1)
    locs = find(centers==i);
    labels = classes(locs);
    clas(i) = mode(labels);
    purity(i) = sum(labels==mode(labels))/size(labels,1);
    wt_pur =wt_pur+ purity(i) * size(labels,1);
end

wt_pur = wt_pur / size(centers,1);
purity=purity';
clas = clas';

function best  = km_eval(data, labels, iter)
best = 0;
for i=1:iter
    km = litekmeans(data', 18);
    [~,wt,~] = purity(km',labels);
    if wt>best
        best = wt
    end
end

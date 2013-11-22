function mat  = sp_read(name)
    files = dir([name '_p*']);
    num = size(files,1);
    for i=0:num-1
        cur = csvread([name '_p' num2str(i)]);
        if i==0
            mat = sparse(cur);
        else
            mat = [mat ; sparse(cur)];
        end
        i
        size(mat)
    end

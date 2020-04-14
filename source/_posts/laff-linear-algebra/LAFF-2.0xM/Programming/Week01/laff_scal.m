function [ x_out ] = laff_scal( alpha, x )

[m,n] = size(x);

if ~isscalar(alpha)
    x_out = 'FAILED';
    return
end
    
if ~isvector(x)
    x_out = 'FAILED';
    return
end

if (m == 1) || (n == 1)
    for i = 1:m
        for j = 1:n
            x(i,j) = alpha * x(i,j);
    x_out = x;
        end
    end
else
    x_out = 'FAILED';
    return
end

return
end

function [ C_out ] = Gemm_unb_var1( A, B, C )

% c_1 := A b_1 + c_1
[ m, n ] = size( C );
[ m_A, k ] = size( A );
[ m_B, n_B ] = size( B );

for i = 1:n_B
    C(:, i) = laff_gemv( 'No transpose',1, A, B(:, i), 1, C(:, i));
end

C_out = C;
end


1 { package_version(P, V) : possible_package_version(P, V) } 1 :- package(P).

possible_package_version(P, V)
    :- declared_package_version(P, V), not disallowed_package_version(P, V).

declared_package_version(p, a).
declared_package_version(p, b).
declared_package_version(p, c).

declared_package_version(q, c).
declared_package_version(q, d).
declared_package_version(q, e).

disallowed_package_version(q, d).
disallowed_package_version(p, c).

% p and q are packages
package(p).
package(q).

#show package_version/2.

% possible results should be:
%
% package_version(p,a) package_version(q,c)
% package_version(p,a) package_version(q,e)
% package_version(p,b) package_version(q,c)
% package_version(p,b) package_version(q,e)

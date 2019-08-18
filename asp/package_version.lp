1 { package_version(P, V) : possible_package_version(P, V) } 1 :- package(P).

possible_package_version(p, a).
possible_package_version(p, b).
possible_package_version(p, c).

possible_package_version(q, c).
possible_package_version(q, d).
possible_package_version(q, e).

% p and q are packages
package(p).
package(q).

#show package_version/2.

% possible results should be:
%
% package_version(p,a) package_version(q,c)
% package_version(p,a) package_version(q,d)
% package_version(p,a) package_version(q,e)
% package_version(p,b) package_version(q,c)
% package_version(p,b) package_version(q,d)
% package_version(p,b) package_version(q,e)
% package_version(p,c) package_version(q,c)
% package_version(p,c) package_version(q,d)
% package_version(p,c) package_version(q,e)

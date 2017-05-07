/**
 * Created by Dvir on 25/04/2017.
 */
function (n) {
    var t, e, r = [];
    n = C(n);
    for (var u = -1, i = this.length; ++u < i;)
        for (var o = this[u], a = -1, c = o.length; ++a < c;)
            (e = o[a]) &&
            (r.push(t = ra(n.call(e, e.__data__, a, u))), t.parentNode = e);
    return A(r);
}
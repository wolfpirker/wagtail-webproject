(function(e) {
    function t(t) {
        for (var r, u, c = t[0], i = t[1], d = t[2], p = 0, s = []; p < c.length; p++) u = c[p], a[u] && s.push(a[u][0]), a[u] = 0;
        for (r in i) Object.prototype.hasOwnProperty.call(i, r) && (e[r] = i[r]);
        f && f(t);
        while (s.length) s.shift()();
        return o.push.apply(o, d || []), n()
    }

    function n() {
        for (var e, t = 0; t < o.length; t++) {
            for (var n = o[t], r = !0, c = 1; c < n.length; c++) {
                var i = n[c];
                0 !== a[i] && (r = !1)
            }
            r && (o.splice(t--, 1), e = u(u.s = n[0]))
        }
        return e
    }
    var r = {},
        a = {
            app: 0
        },
        o = [];

    function u(t) {
        if (r[t]) return r[t].exports;
        var n = r[t] = {
            i: t,
            l: !1,
            exports: {}
        };
        return e[t].call(n.exports, n, n.exports, u), n.l = !0, n.exports
    }
    u.m = e, u.c = r, u.d = function(e, t, n) {
        u.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: n
        })
    }, u.r = function(e) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }, u.t = function(e, t) {
        if (1 & t && (e = u(e)), 8 & t) return e;
        if (4 & t && "object" === typeof e && e && e.__esModule) return e;
        var n = Object.create(null);
        if (u.r(n), Object.defineProperty(n, "default", {
                enumerable: !0,
                value: e
            }), 2 & t && "string" != typeof e)
            for (var r in e) u.d(n, r, function(t) {
                return e[t]
            }.bind(null, r));
        return n
    }, u.n = function(e) {
        var t = e && e.__esModule ? function() {
            return e["default"]
        } : function() {
            return e
        };
        return u.d(t, "a", t), t
    }, u.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, u.p = "";
    var c = window["webpackJsonp"] = window["webpackJsonp"] || [],
        i = c.push.bind(c);
    c.push = t, c = c.slice();
    for (var d = 0; d < c.length; d++) t(c[d]);
    var f = i;
    o.push([0, "chunk-vendors"]), n()
})({
    0: function(e, t, n) {
        e.exports = n("56d7")
    },
    "56d7": function(e, t, n) {
        "use strict";
        n.r(t);
        n("cadf"), n("551c"), n("f751"), n("097d");
        var r = n("2b0e"),
            a = function() {
                var e = this,
                    t = e.$createElement,
                    n = e._self._c || t;
                return n("div", {
                    attrs: {
                        id: "app"
                    }
                }, [n("VRangeSelector", {
                    attrs: {
                        "start-date": e.range.start,
                        "end-date": e.range.end
                    },
                    on: {
                        "update:startDate": function(t) {
                            return e.$set(e.range, "start", t)
                        },
                        "update:start-date": function(t) {
                            return e.$set(e.range, "start", t)
                        },
                        "update:endDate": function(t) {
                            return e.$set(e.range, "end", t)
                        },
                        "update:end-date": function(t) {
                            return e.$set(e.range, "end", t)
                        }
                    }
                }), n("div", [e._v("Selected range:")]), n("div", [e._v("Start: " + e._s(e.range.start))]), n("div", [e._v("End: " + e._s(e.range.end))])], 1)
            },
            o = [],
            u = n("c69d"),
            c = {
                name: "App",
                data: function() {
                    return {
                        range: {}
                    }
                },
                components: {
                    VRangeSelector: u["a"]
                }
            },
            i = c,
            d = (n("5c0b"), n("2877")),
            f = Object(d["a"])(i, a, o, !1, null, null, null),
            p = f.exports;
        r["a"].config.productionTip = !1, new r["a"]({
            render: function(e) {
                return e(p)
            }
        }).$mount("#app")
    },
    "5c0b": function(e, t, n) {
        "use strict";
        var r = n("e332"),
            a = n.n(r);
        a.a
    },
    e332: function(e, t, n) {}
});
//# sourceMappingURL=app.58971650.js.map

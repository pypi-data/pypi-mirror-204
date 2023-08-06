from fastcons import cons, nil

from microkanren import (
    Hooks,
    conj,
    disj,
    eq,
    fresh,
    process_prefix_neq,
    run,
)
from microkanren.goals import appendo, caro, cdro, conso

Hooks.set_process_prefix(process_prefix_neq)


class Symbol(type):
    _syms = {}

    def __new__(cls, name, bases, _dict):
        newtype = super().__new__(cls, name, bases, _dict)
        cls._syms[newtype] = name
        return newtype

    def __repr__(self):
        return self._syms[self]

    def __getitem__(self, key):
        return [self, key]


class λ(metaclass=Symbol):
    def __new__(cls):
        return cls


class NMeta(Symbol):
    def __getitem__(self, i):
        return cons.from_xs(N for _ in range(i))


class N(metaclass=NMeta):
    def __new__(cls):
        return cls


def reify_value(value):
    match value:
        case nil():
            return 0
        case cons(a, _) if a is N:
            return len(value.to_list())
        case cons(a, d):
            return cons(reify_value(a), reify_value(d))
        case xs if isinstance(xs, list | tuple):
            return type(xs)(reify_value(x) for x in value)
        case _:
            return value


Hooks.set_reify_value(reify_value)


def pairo(p):
    return fresh(lambda a, d: conso(a, d, p))


def zero(i):
    return eq(i, N[0])


def one(i):
    return eq(i, N[1])


def succ(x, y):
    return conso(N, x, y)


def numbero(n):
    return eq(n, N[0]) | fresh(lambda d: conso(N, d, n) & numbero(d))


def positive(n):
    return conso(N, nil(), n) | fresh(lambda m: succ(m, n) & positive(m))


def gt(j, q):
    """j > q"""

    def _gt(i, p):
        return disj(
            zero(q) & positive(j),
            succ(i, j) & succ(p, q) & gt(i, p),
        )

    return fresh(_gt)


def gte(j, q):
    def _gte(i, p):
        return disj(
            gt(j, q),
            numbero(j) & numbero(q) & eq(j, q),
            succ(i, j) & succ(p, q) & gte(i, j),
        )

    return fresh(_gte)


def length(ls, x):
    return disj(
        eq(nil(), ls) & eq(x, N[0]),
        fresh(
            lambda a, d, res: conso(a, d, ls) & succ(res, x) & length(d, res),
        ),
    )


### basics
id = λ[N[0]]

### bools, conditionals
iff = id


def mkif(p, c, a):
    return ((iff, p), c), a


true = λ[λ[N[1]]]
false = λ[λ[N[0]]]

### data structures
empty = false
# pair = λx.λy.λf.f x y
pair = λ[λ[λ[((N[0], N[2]), N[1])]]]


def mkpair(x, y):
    return (pair, x), y


head = λ[(N[0], true)]
tail = λ[(N[0], false)]


def free_var(t, binders):
    return gte(t, binders)


def free_vars(t, binders, vs):
    def _free_vars(m, n, bs, cs):
        return disj(
            conj(
                abstraction(m, t),
                succ(binders, bs),
                free_vars(m, bs, vs),
            ),
            conj(
                application(m, n, t),
                free_vars(m, binders, bs),
                free_vars(n, binders, cs),
                appendo(bs, cs, vs),
            ),
            numbero(t)
            & disj(
                gte(t, binders) & conso(t, nil(), vs),
                gt(binders, t) & eq(vs, nil()),
            ),
        )

    return fresh(_free_vars)


def closed_term(t):
    return free_vars(t, nil(), nil())


def term(t):
    return disj(
        numbero(t),
        fresh(lambda m, n: application(m, n, t)),
        fresh(lambda m: abstraction(m, t)),
    )


def application(rator, rand, t):
    return eq(t, (rator, rand)) & term(rator) & term(rand)


def abstraction(body, t):
    return eq(t, [λ, body]) & term(body)


def k_eval(t, out):
    return conj(
        closed_term(t),
        k(t, nil(), nil(), out),
    )


def k(t, e, p, out):
    def _k():
        return disj(
            push(t, e, p, out),
            pop(t, e, p, out),
            goto(t, e, p, out),
        )

    return fresh(_k)


def push(t, e, p, out):
    def _push(rator, rand, next_stack):
        return conj(
            application(rator, rand, t),
            conso(cons(rand, e), p, next_stack),
            k(rator, e, next_stack, out),
        )

    return fresh(_push)


def pop(t, e, p, out):
    def _pop(body, top_p, rest_ps, next_env):
        return conj(
            abstraction(body, t),
            disj(
                conj(
                    conso(top_p, rest_ps, p),
                    conso(top_p, e, next_env),
                    k(body, next_env, rest_ps, out),
                ),
                conj(
                    eq(p, nil()),
                    eq(t, out),
                ),
            ),
        )

    return fresh(_pop)


def goto(t, e, p, out):
    def _goto(s, es, f, i):
        return disj(
            succ(s, t) & cdro(es, e) & k(s, es, p, out),
            zero(t) & caro(cons(i, f), e) & k(i, f, p, out),
        )

    return fresh(_goto)


if __name__ == "__main__":
    print(run(5, lambda x: k_eval(x, true)))

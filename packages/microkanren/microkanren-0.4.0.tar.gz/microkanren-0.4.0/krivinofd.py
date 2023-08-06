from fastcons import cons, nil

from microkanren.core import (
    Hooks,
    compose_constraints,
    conj,
    disj,
    eq,
    fresh,
    process_prefix_neq,
    run,
)
from microkanren.fd import (
    domfd,
    enforce_constraints_fd,
    ltefd,
    ltfd,
    mkrange,
    plusfd,
    process_prefix_fd,
)
from microkanren.goals import appendo, caro, cdro, conso

Hooks.set_process_prefix(
    lambda p, c: compose_constraints(process_prefix_neq(p, c), process_prefix_fd(p, c))
)
Hooks.set_enforce_constraints(enforce_constraints_fd)


class Symbol(type):
    _syms = {}

    def __new__(cls, name, bases, _dict):
        newtype = super().__new__(cls, name, bases, _dict)
        cls._syms[newtype] = name
        return newtype

    def __repr__(self):
        return self._syms[self]

    def __getitem__(self, key):
        return cons(self, key)


class λ(metaclass=Symbol):
    def __new__(cls):
        return cls


def pairo(p):
    return fresh(lambda a, d: conso(a, d, p))


def zero(i):
    return eq(i, 0)


def one(i):
    return eq(i, 1)


def succ(x, y):
    return plusfd(x, 1, y)


def numbero(n):
    return domfd(n, mkrange(0, 256))


def positive(n):
    return domfd(n, mkrange(1, 256))


### basics
id = λ[0]

### bools, conditionals
iff = id


def mkif(p, c, a):
    return ((iff, p), c), a


true = λ[λ[1]]
false = λ[λ[0]]

### data structures
empty = false
# pair = λx.λy.λf.f x y
pair = λ[λ[λ[((0, 2), 1)]]]


def mkpair(x, y):
    return (pair, x), y


head = λ[(0, true)]
tail = λ[(0, false)]


def free_var(t, depth):
    return numbero(t) & numbero(depth) & ltefd(depth, t)


def _free_vars(t, depth, vs):
    return numbero(depth) & disj(
        conj(
            numbero(t),
            ltfd(t, depth),
            eq(vs, nil()),
        ),
        conj(
            numbero(t),
            ltefd(depth, t),
            eq(cons(t, nil()), vs),
        ),
        fresh(
            lambda body, e: conj(
                abstraction(body, t),
                succ(depth, e),
                _free_vars(body, e, vs),
            ),
        ),
        fresh(
            lambda p, q, ps, qs: conj(
                application(p, q, t),
                _free_vars(p, depth, ps),
                _free_vars(q, depth, qs),
                appendo(ps, qs, vs),
            ),
        ),
    )


def free_vars(t, vs):
    return _free_vars(t, 0, vs)


def closed_term(t):
    return free_vars(t, nil())


def term(t):
    return disj(
        numbero(t),
        fresh(lambda m, n: application(m, n, t)),
        fresh(lambda m: abstraction(m, t)),
    )


def application(rator, rand, t):
    return eq(t, (rator, rand)) & term(rator) & term(rand)


def abstraction(body, t):
    return eq(t, cons(λ, body)) & term(body)


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

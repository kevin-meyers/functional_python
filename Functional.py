def identity(x):
    return x

def fold(combining_function, xs, initial_accumulator):
    accumulator = initial_accumulator
    for x in xs:
        accumulator = combining_function(x, accumulator)

    return accumulator

def compose_2(function_1, function_2):
    return lambda x: function_1(function_2(x))

def compose(functions):
    return fold(compose_2, functions, identity)

def fmap(function, functor):
    # if isinstance(functor, list):

    return functor.fmap(function)

def lift(function):
    return lambda functor: fmap(function, functor)

class Functor:
    def __init__(self, val):
        self.val = val

    def fmap(self, func):
        raise NotImplementedError

class Maybe(Functor):
    def __repr__(self):
        if self.val is None:
            return 'Nothing'

        return f'Just {repr(self.val)}'

    def fmap(self, func):
        if self.val is None:
            return self

        return Maybe(func(self.val))

    def case(self, default_value, function):
        if self.val is None:
            return default_value

        return function(self.val)


class Either(Functor):
    pass

class Left(Either):
    def __repr__(self):
        return f'Left {self.val}'

    def fmap(self, _):
        return self

    def case(self, if_left_function, _):
        return if_left_function(self.val)

class Right(Either):
    def __repr__(self):
        return f'Right {self.val}'

    def fmap(self, function):
        # what if the function returns a left? or a nothing?
        return Right(function(self.val))

    def case(self, _, if_right_function):
        return if_right_function(self.val)

def author_conditions_for_posts(query_result):
    mIds = Maybe(query_result)
    return mIds.case(
        Left("{author_id} doesn't seem to exist in this dimension."),
        lambda ids: Right(
            ids['parent_id'].case(
                Right(count_maybes(map(
                    lambda method: fmap(
                        lambda x: '12345' == x, 
                        ids[method]
                    ),
                    ["t_id", "g_id", "c_id"]
                ))),
                lambda parent_id: Left(parent_id)
            )
        )
    )

def count_maybes(mList):
    return sum(1 for x in mList if x.val is not None)

def test_author_post(eConditions):
    return eConditions.case(
        lambda error: f'HTTPError(404, {error})',
        lambda eCondOrRedirect: eCondOrRedirect.case(
            lambda parent_id: f'I get redirected to /author/{parent_id}/...',
            identity
        )
    )

def run_test_author_post(fake_query):
    result = author_conditions_for_posts(fake_query)
    return test_author_post(result)

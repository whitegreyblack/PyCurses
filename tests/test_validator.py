from source.validator import Validator, Example

def test_empty_validator():
    v = Validator()
    assert v({}) == True
    assert v({'a':123}) == True

def test_empty_validator_on_dict():
    v = Validator()
    assert v(Example()) == True

def test_validate_single_int_with_dict_single_int():
    v = Validator({'a':{'type':'int'}})
    assert v({'a':2}) == True

def test_single_int_correct_validator_on_dict():
    v = Validator({'a':{'type':'int'}})
    assert v({'a':2}) == True

def test_single_int_correct_validator_on_class():
    v = Validator({'a':{'type':'int'}})
    assert v(Example()) == True

def test_single_int_incorrect_validator_on_dict():
    v = Validator({'a':{'type':'int'}})
    assert v({'a':'v'}) == False

def test_single_str_correct_validator_on_dict():
    v = Validator({'a':{'type':'str'}})
    assert v({'a':'abc'}) == True

if __name__ == "__main__":
    # small tests
    
    # test on an empty validator
    t = Validator()
    print(t(Example()))

    # create a validator v with some attributes
    v = Validator({'a':{'type':'int'}, 'b':{'type':'int'}})
    print(v)

    # option 1: pass in as dict
    print("v({'a':3, 'b':4}):", v({'a':3, 'b':4}))
    print("v({'a':3, 'b':'a'}):", v({'a':3, 'b':'a'}))
    
    # using class with attributes pulled with __dict__
    print("v(Example()):", v(Example()))
    print("v(Example(3, 'a')):", v(Example(3, 'a')))

    # Exception cases
    # skips args but raises error on nonmatching attribute
    bypass(v, 3)
    # adds kwargs to validator but missing other attributes
    bypass(v, {'c':5})

    # create a validator v with different definitions than v
    w = Validator({'a':{'type':'int'}, 'b':{'type':'str'}}, exceptions=True)
    print(w)

    # given an (int, int) validated by an (int, str)
    # the validator should check the second attribute
    e = Example(2, 2)
    print("w(e):", w(e))

    # try the same example again but with a dictionary object
    # instead of a class object. Using w returns false, v returns true.
    d = {'a':3, 'b':4}
    print("w(d):", w(d))
    print("v(d):", v(d))

    # TODO: nested objects using iterables
    x = Validator({'a': (list, {'el': int})})
    print(x)
    x({'a': [1,2,3]})
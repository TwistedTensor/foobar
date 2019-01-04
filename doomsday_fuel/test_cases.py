from doomsday_fuel import *
test_cases = [
    {
        'm':[[0, 1, 0, 0, 0, 1], 
             [4, 0, 0, 3, 2, 0], 
             [0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0]],
        'answer':[0, 3, 2, 9, 14]
    },
    {
        'm':[[0, 2, 1, 0, 0], 
             [0, 0, 0, 3, 4], 
             [0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0]],
        'answer':[7, 6, 8, 21]
    }
]
for i,test in enumerate(test_cases):
    result = answer(test['m'])
    if result==test['answer']:
        print 'test {} passed'.format(i)
    else:
        print 'test {} failed'.format(i)
        print 'expected {}, got {}'.format(test['answer'],result)

def apply(list, n, d):
    res = []
    for elem in list:
        res.append((elem ** d) % n)
    return res

def get_letters(nums):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    res = ""
    for num in nums:
        res += letters[num % 26]
    return res

if __name__ == "__main__":
    nums = apply([138527, 171279, 138664, 242409, 103298, 171279, 27261,103786, 0, 103298, 0, 103298, 242409, 224525, 188808, 171279, 27261], 256961, 13)
    print(get_letters(nums))

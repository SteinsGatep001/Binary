#include <stdio.h>
constexpr char FLAG[] = "Please_Input_The_Flag";  //input the flag !!!



template <int _, int __> struct ___Fun1___ { enum { ___ = (_ == __) }; };
template <int _, int __> struct ___fun2___ { enum { ___ = (_ ^ __) }; };
template <int __> struct ___fun3___{enum { ___ = FLAG[__] };};
template <int _,int __> struct ___fun4___{enum{___ = _ % __}; };
template<int _, int __> struct ___fun5___ { const static int ___ = __ << _; };
template<int _, int __> struct ___fun6___ { const static int ___ = __ >> _; };
template<int _, int __> struct ___fun7___ { const static int ___ = _ & __; };
template<int _, int __> struct ___fun8___ { const static int ___ = _ | __; };
template <int __> struct ___fun9___ { enum { ___ = __+___fun9___<__ - 1>::___ }; };
template <> struct ___fun9___<0> { enum { ___ = 0 }; };
template <int __> struct ___fun10___ { enum { ___ = ___Fun1___<(sizeof(FLAG) - 1), __>::___ }; };
template <int _, int __> struct ___fun11___{enum {___ = ___Fun1___<___fun2___<___fun3___<_>::___,0x20>::___,93>::___};};
template <int _> struct ___fun11___<_, 0> {enum { ___ = 0 };};
constexpr int ___Arr1___[] = { 88,83,68,86,75 };
template <int _> struct ___fun12___ { enum { ___ = ___Arr1___[_] }; };
template<int _, int __> struct ___fun13___{ enum { ____ = ___fun13___<_-1,___Fun1___<___fun12___<_>::___, ___fun2___<___fun3___<_>::___, 0x30>::___>::___>::____};};
template<int _> struct ___fun13___<_, 1>{enum { ____ = ___fun13___<_ - 1, ___Fun1___<___fun12___<_>::___, ___fun2___<___fun3___<_>::___, 0x30>::___>::___>::____}; };
template<> struct ___fun13___<-1,1>{	enum { ____ = 1 };};
template<int _> struct ___fun13___<_, 0> {enum { ____ = 0 }; };
template<int _, int __> struct ___fun14___ { enum { ___ = 0 }; };
template<int _> struct ___fun14___<_, 0> { enum { ___ = (___fun3___<_ + 5* ___fun10___<26>::___>::___ + _) }; };
template<int _> struct ___fun14___<_, 1> { enum { ___ = (___fun3___<_ + 5* ___fun10___<26>::___>::___ - _) }; };
template<int _> struct ___fun15___ {enum {___ = ___fun2___<___fun9___<_>::___, 106>::___}; };
template<int _> struct ___fun16___{enum{___ = ___fun2___<___fun14___<_, ___fun4___<_,2>::___>::___, ___fun15___<_>::___>::___};};
template<int _> struct ___fun17___ { const static int ___ = ___fun8___<___fun6___<4, _>::___, ___fun5___<4, ___fun7___<_, 0xF>::___>::___>::___; };
template<int _> struct ___fun18___ { const static int ___ = ___fun2___<___fun17___<___fun16___<_>::___>::___, ___fun18___<_ - 1>::___>::___; };
template <> struct ___fun18___<0> { const static int ___ = ___fun17___<___fun16___<0>::___>::___; };
constexpr int ___Arr2___[] = { 0x93,0xd7, 0x57, 0xb5, 0xe5, 0xb0, 0xb0, 0x52, 0x2, 0x0, 0x72, 0xb5, 0xf1, 0x80, 0x7, 0x30, 0xa, 0x30, 0x44, 0xb };
template <int _> struct ___fun19___ { enum { ___ = ___Arr2___[_] }; };
template <int _, int __> struct ___fun20___ { enum {___ = ___fun20___<_+1, ___Fun1___< ___fun19___<_>::___, ___fun18___<_>::___>::___>::___}; };
template <> struct ___fun20___<20,1> {enum {___  = 1}; };
template <int _> struct ___fun20___<_, 0> { enum { ___ = 0 }; };
template <int __> struct ___fun21___{enum { ___ = ___fun11___<26- __,___fun13___<4, 1>::____>::___ };};
template <> struct ___fun21___ <0> { enum { ___ = 0 }; };



struct __Start
{
	enum
	{
		ret = ___fun20___<0, ___fun21___<___fun10___<26>::___>::___>::___
	};
};


int main()
{
	if (__Start::ret)
	{
		printf("Yes,You got it\n");
	}
	else
	{
		printf("Sorry,try again\n");
	}
	return 0;
}

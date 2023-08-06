#include "c4/std/string.hpp"
#include "c4/std/vector.hpp"
#include "c4/test.hpp"
#include "c4/format.hpp"

#include "c4/libtest/supprwarn_push.hpp"

namespace c4 {


//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

template<class T>
void test_to_chars_fmt_basic(T f, int precision, const char* flt, T fltv, const char *scient, T scientv)
{
    char bufc[64];
    substr buf(bufc);
    substr r;
    T copy;

    r = to_chars_sub(buf, fmt::fmt(f, precision));
    EXPECT_EQ(r, to_csubstr(flt)) << "num=" << f;
    from_chars(r, &copy);
    if(sizeof(T) == sizeof(float))
    {
        EXPECT_FLOAT_EQ((float)fltv, (float)copy);
    }
    else
    {
        EXPECT_DOUBLE_EQ(fltv, copy);
    }

    r = to_chars_sub(buf, fmt::fmt(f, precision, FTOA_SCIENT));
    EXPECT_EQ(r, to_csubstr(scient)) << "num=" << f;
    from_chars(r, &copy);
    if(sizeof(T) == sizeof(float))
    {
        EXPECT_FLOAT_EQ((float)scientv, (float)copy);
    }
    else
    {
        EXPECT_DOUBLE_EQ(scientv, copy);
    }
}

TEST(to_chars, fmt_basic)
{
    char bufc[128];
    substr buf(bufc);

    EXPECT_EQ(to_chars_sub(buf, fmt::hex( int8_t(0x7f))), "0x7f");
    EXPECT_EQ(to_chars_sub(buf, fmt::hex(uint8_t(0xff))), "0xff");

    float f = 256.064f;
    test_to_chars_fmt_basic<float>(f, 0, "256", 256.f, "3e+02", 300.f);
    test_to_chars_fmt_basic<float>(f, 1, "256.1", 256.1f, "2.6e+02", 260.f);
    test_to_chars_fmt_basic<float>(f, 2, "256.06", 256.06f, "2.56e+02", 256.f);
    test_to_chars_fmt_basic<float>(f, 3, "256.064", 256.064f, "2.561e+02", 256.1f);
    test_to_chars_fmt_basic<float>(f, 4, "256.0640", 256.0640f, "2.5606e+02", 256.06f);
    test_to_chars_fmt_basic<float>(f, 5, "256.06400", 256.06400f, "2.56064e+02", 256.064f);

    double d = 256.064;
    test_to_chars_fmt_basic<double>(d, 0, "256", 256., "3e+02", 300.);
    test_to_chars_fmt_basic<double>(d, 1, "256.1", 256.1, "2.6e+02", 260.);
    test_to_chars_fmt_basic<double>(d, 2, "256.06", 256.06, "2.56e+02", 256.);
    test_to_chars_fmt_basic<double>(d, 3, "256.064", 256.064, "2.561e+02", 256.1);
    test_to_chars_fmt_basic<double>(d, 4, "256.0640", 256.0640, "2.5606e+02", 256.06);
    test_to_chars_fmt_basic<double>(d, 5, "256.06400", 256.06400, "2.56064e+02", 256.064);
}


//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

TEST(cat, vars)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = cat(buf, 1, ' ', 2, ' ', 3, ' ', 4);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2 3 4");
}

#ifdef C4_TUPLE_TO_STR
TEST(cat, tuple)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = cat(buf, std::forward_as_tuple(1, ' ', 2, ' ', 3, ' ', 4));
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2 3 4");
}
#endif // C4_TUPLE_TO_STR

TEST(uncat, vars)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;

    sz = uncat("1 2 3 4", v1, v2, v3, v4);
    EXPECT_NE(sz, csubstr::npos);
    EXPECT_EQ(sz, 7);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}

#ifdef C4_TUPLE_TO_STR
TEST(uncat, tuple)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;

    auto tp = std::forward_as_tuple(v1, v2, v3, v4);
    sz = uncat("1 2 3 4", tp);
    EXPECT_NE(sz, csubstr::npos);
    EXPECT_EQ(sz, 7);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}
#endif // C4_TUPLE_TO_STR

TEST(catsep, vars)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = catsep(buf, ' ', 1, 2);
    EXPECT_EQ(sz, 3);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2");

    sz = catsep(buf, '/', 1, 2);
    EXPECT_EQ(sz, 3);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1/2");

    sz = catsep(buf, ' ', 1, 2, 3, 4);
    EXPECT_EQ(sz, 7);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2 3 4");

    sz = catsep(buf, '/', 1, 2, 3, 4);
    EXPECT_EQ(sz, 7);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1/2/3/4");
}

#ifdef C4_TUPLE_TO_STR
TEST(catsep, tuple)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = catsep(buf, ' ', std::forward_as_tuple(1, 2));
    EXPECT_EQ(sz, 3);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2");

    sz = catsep(buf, '/', std::forward_as_tuple(1, 2));
    EXPECT_EQ(sz, 3);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1/2");

    sz = catsep(buf, ' ', std::forward_as_tuple(1, 2, 3, 4));
    EXPECT_EQ(sz, 7);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 2 3 4");

    sz = catsep(buf, '/', std::forward_as_tuple(1, 2, 3, 4));
    EXPECT_EQ(sz, 7);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1/2/3/4");
}
#endif // C4_TUPLE_TO_STR

TEST(uncatsep, vars)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;
    char sep;

    sz = uncatsep("1 2 3 4", sep, v1, v2, v3, v4);
    EXPECT_EQ(sz, 7);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}

#ifdef C4_TUPLE_TO_STR
TEST(uncatsep, tuple)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;
    char sep;

    auto tp = std::forward_as_tuple(v1, v2, v3, v4);
    sz = uncatsep("1 2 3 4", sep, tp);
    EXPECT_EQ(sz, 7);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}
#endif // C4_TUPLE_TO_STR

TEST(format, vars)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = format(buf, "{} and {} and {} and {}", 1, 2, 3, 4);
    EXPECT_EQ(sz, 19);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and 4");

    sz = format(buf, "{} and {} and {} and {}", 1, 2, 3, 4, 5, 6, 7);
    EXPECT_EQ(sz, 19);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and 4");

    sz = format(buf, "{} and {} and {} and {}", 1, 2, 3);
    EXPECT_EQ(sz, 20);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and {}");

    sz = format(buf, "{} and {} and {} and {}", 1, 2);
    EXPECT_EQ(sz, 21);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and {} and {}");

    sz = format(buf, "{} and {} and {} and {}", 1);
    EXPECT_EQ(sz, 22);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and {} and {} and {}");

    sz = format(buf, "{} and {} and {} and {}");
    EXPECT_EQ(sz, 23);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "{} and {} and {} and {}");
}

#ifdef C4_TUPLE_TO_STR
TEST(format, tuple)
{
    char buf[256];
    substr sp(buf);
    csubstr result;
    size_t sz;

    sz = format(buf, "{} and {} and {} and {}", std::forward_as_tuple(1, 2, 3, 4));
    EXPECT_EQ(sz, 19);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and 4");

    sz = format(buf, "{} and {} and {} and {}", std::forward_as_tuple(1, 2, 3, 4, 5, 6, 7));
    EXPECT_EQ(sz, 19);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and 4");

    sz = format(buf, "{} and {} and {} and {}", std::forward_as_tuple(1, 2, 3));
    EXPECT_EQ(sz, 20);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and 3 and {}");

    sz = format(buf, "{} and {} and {} and {}", std::forward_as_tuple(1, 2));
    EXPECT_EQ(sz, 21);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and 2 and {} and {}");

    sz = format(buf, "{} and {} and {} and {}", std::forward_as_tuple(1));
    EXPECT_EQ(sz, 22);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "1 and {} and {} and {}");

    sz = format(buf, "{} and {} and {} and {}");
    EXPECT_EQ(sz, 23);
    result = sp.left_of(sz);
    EXPECT_EQ(result, "{} and {} and {} and {}");
}
#endif // C4_TUPLE_TO_STR

TEST(unformat, vars)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;

    sz = unformat("1 and 2 and 3 and 4", "{} and {} and {} and {}", v1, v2, v3, v4);
    EXPECT_EQ(sz, 19);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}

#ifdef C4_TUPLE_TO_STR
TEST(unformat, tuple)
{
    size_t sz;
    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;

    auto tp = std::forward_as_tuple(v1, v2, v3, v4);
    sz = unformat("1 and 2 and 3 and 4", "{} and {} and {} and {}", tp);
    EXPECT_EQ(sz, 19);
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
    EXPECT_EQ(v4, 4);
}
#endif // C4_TUPLE_TO_STR


TEST(printf, basic)
{
    char bufc[128];
    substr buf = bufc;
    size_t ret;

    memset(buf.str, 0, buf.len);
    ret = sprintf(buf, "hello world");
    EXPECT_EQ(buf.first(ret), "hello world");

    memset(buf.str, 0, buf.len);
    ret = sprintf(buf, "%d %d %d %d", 1, 2, 3, 4);
    EXPECT_EQ(buf.first(ret), "1 2 3 4");
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
TEST(catrs, basic)
{
    std::vector<char> buf;

    catrs(&buf, 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1234");
    catrs(&buf, 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "5678");
}

TEST(catrs, basic_append)
{
    std::vector<char> buf;

    catrs(append, &buf, 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1234");
    catrs(append, &buf, 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "12345678");
    catrs(append, &buf, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "123456789012345678");
}

TEST(catseprs, basic)
{
    std::vector<char> buf;

    catseprs(&buf, ' ', 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1 2 3 4");
    catseprs(&buf, ' ', 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "5 6 7 8");

    catseprs(&buf, ',', 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1,2,3,4");
    catseprs(&buf, ',', 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "5,6,7,8");

    catseprs(&buf, '/', 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1/2/3/4");
    catseprs(&buf, '/', 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "5/6/7/8");

    catseprs(&buf, "///", 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1///2///3///4");
    catseprs(&buf, "///", 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "5///6///7///8");
}

TEST(catseprs, basic_append)
{
    std::vector<char> buf;

    catseprs(append, &buf, ' ', 1, 2, 3, 4);
    EXPECT_EQ(to_csubstr(buf), "1 2 3 4");
    catseprs(append, &buf, ' ', 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "1 2 3 45 6 7 8");
    catseprs(append, &buf, ' ', 9, 0, 1, 2, 3, 4, 5, 6, 7, 8);
    EXPECT_EQ(to_csubstr(buf), "1 2 3 45 6 7 89 0 1 2 3 4 5 6 7 8");
}

TEST(formatrs, basic)
{
    std::vector<char> buf;

    formatrs(&buf, "{} goes with food, {} goes with heat, {} anytime", "wine", "beer", "coffee");
    EXPECT_EQ(to_csubstr(buf), "wine goes with food, beer goes with heat, coffee anytime");
}

TEST(formatrs, basic_append)
{
    std::vector<char> buf;

    formatrs(append, &buf, "{} goes with food", "wine");
    EXPECT_EQ(to_csubstr(buf), "wine goes with food");
    formatrs(append, &buf, ", {} goes with heat", "beer");
    EXPECT_EQ(to_csubstr(buf), "wine goes with food, beer goes with heat");
    formatrs(append, &buf, ", {} anytime", "coffee");
    EXPECT_EQ(to_csubstr(buf), "wine goes with food, beer goes with heat, coffee anytime");

    formatrs(append, &buf, ". And water. {} glass of {}cl in the morning clears you up for the day", 1, 40);
    EXPECT_EQ(to_csubstr(buf), "wine goes with food, beer goes with heat, coffee anytime. And water. 1 glass of 40cl in the morning clears you up for the day");
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
TEST(fmt, hex)
{
    std::vector<char> buf;
    char buf1[1] = {};
    char buf2[2] = {};
    char buf3[3] = {};

#define _(in, expected_)                                            \
    {                                                               \
        auto expected = csubstr(expected_);                         \
        EXPECT_EQ(cat({}, fmt::hex(in)), expected.len);             \
                                                                    \
        std::cout << "AQUI 0\n";                                    \
        buf1[0] = '?';                                              \
        EXPECT_EQ(cat(buf1, fmt::hex(in)), expected.len);           \
        EXPECT_EQ(buf1[0], '?');                                    \
                                                                    \
        std::cout << "AQUI 1\n";                                    \
        buf2[0] = '?';                                              \
        buf2[1] = '?';                                              \
        EXPECT_EQ(cat(buf2, fmt::hex(in)), expected.len);           \
        EXPECT_EQ(buf2[0], '0');                                    \
        EXPECT_EQ(buf2[1], '?');                                    \
                                                                    \
        std::cout << "AQUI 2\n";                                    \
        buf3[0] = '?';                                              \
        buf3[1] = '?';                                              \
        buf3[2] = '?';                                              \
        EXPECT_EQ(cat(buf3, fmt::hex(in)), expected.len);           \
        EXPECT_EQ(buf3[0], '0');                                    \
        EXPECT_EQ(buf3[1], 'x');                                    \
        EXPECT_EQ(buf3[2], '?');                                    \
                                                                    \
        std::cout << "AQUI 3\n";                                    \
        buf.clear();                                                \
        EXPECT_EQ(cat(to_substr(buf), fmt::hex(in)), expected.len); \
        EXPECT_EQ(buf.size(), 0);                                   \
                                                                    \
        catrs(&buf, fmt::hex(in));                                  \
        EXPECT_EQ(buf.size(), expected.len);                        \
        EXPECT_EQ(to_csubstr(buf), expected);                       \
    }

    _(0, "0x0");
    _(nullptr, "0x0");
    _(256, "0x100");

#undef _
}


//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

template<class T> void raw_roundtrip(const char *valstr, T const& orig)
{
    SCOPED_TRACE(valstr);
    alignas(alignof(T)) char buf_[2 * (sizeof(T) + alignof(T))] = {};
    substr buf = buf_;

    fmt::const_raw_wrapper rawwrap = fmt::craw(orig);
    ASSERT_EQ((void*)rawwrap.buf, (void*)&orig);
    ASSERT_EQ(rawwrap.len, sizeof(orig));

    for(size_t i = 0; i < alignof(T); ++i)
    {
        // make sure to cover unaligned buffers
        substr sbuf = buf.sub(i);
        size_t szwrite = c4::to_chars(sbuf, fmt::craw(orig));
        ASSERT_LE(szwrite, sbuf.len) << i;
        if(i == 0)
        {
            ASSERT_EQ(szwrite, sizeof(T)) << i;
        }
        else
        {
            ASSERT_GT(szwrite, sizeof(T)) << i;
        }
        T copy = {};
        ASSERT_NE(copy, orig) << i;
        size_t szread = c4::from_chars(sbuf, fmt::raw(copy));
        ASSERT_EQ(szread, szwrite) << i;
        EXPECT_EQ(copy, orig) << i;

        // cover also insufficient buffers
        sbuf = sbuf.first(sizeof(T)-1);
        memset(buf.str, 0, buf.len);
        szwrite = c4::to_chars(sbuf, fmt::craw(orig));
        ASSERT_GT(szwrite, sbuf.len) << i;
        for(char c : buf)
        {
            EXPECT_EQ(c, 0) << "i=" << i;
        }
    }
}

TEST(fmt, raw_int)
{
    #define _(v) raw_roundtrip(#v, v)

    _(int(1));
    _(int(2));
    _(int(-1));
    _(int(-2));

    #undef _
}

} // namespace c4

#include "c4/libtest/supprwarn_pop.hpp"

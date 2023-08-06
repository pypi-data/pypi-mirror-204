# Compares 2 texts with each other, and returns a Pandas DataFrame

```python
pip install a-pandas-ex_text-compare
```

```python
from a_pandas_ex_text_compare import pd_add_text_difference
import pandas as pd

pd_add_text_difference()



# Examples of possible inputs (bytes, list, string, path (as string))

text1 = """  1. Beautiful isxx better than ugly.
  2. Explicit isq better than implicit.
  3. Simple is better than complex.
  4. Complex is better than complicated.
"""

text2 = """  
1. Beautiful is better than ugly.
  2. Explicit is better than implicit.
  3. qSimple is better than pcomplex.
  4. Complicated aais better than complex.
  5. Flat is better than nested.
""".splitlines(
    keepends=True
)
text2 = '''The green man wakes and sees her place
The spectacles upon her face;
And now she's trying all she can
To shoot the sleepy, green-coat man.
He cries and screams and runs away;
The hare runs after him all day
The hare runs after him all day
And hears him call out everywhere:
"Help! Fire! Help! The Hare! The Hare!"'''.encode()

text1 = b'''The yellow man wakes and sees her place
The spectacles upon her face;
The spectacles upon her face;
And now she is trying all that she can
To shoot the tired, green-coat man.
He cries and screams and runs away;
The hare runs after him the whole day
And hears him call out everywhere:
and hears him call out everywhere:
"Help! Fire! Help! The Hare! The Hare!"'''

text1 = r"C:\Users\Gamer\Documents\Downloads\testread.txt"


df = pd.Q_text_difference_to_df(text1, text2, encoding="utf-8")
print(df.to_string())

"""
    no                                  aa_text                                  bb_text                            aa_added                   bb_substracted aa_changed bb_changed                                         aa_diff                                      bb_diff                                          aa_parts                                           bb_parts
0    0   The green man wakes and sees her place  The yellow man wakes and sees her place                                <NA>                             <NA>          y         gr                                   (diff_chg, y)                               (diff_chg, gr)  (The , gr, e, en,  man wakes and sees her place)  (The , y, e, llow,  man wakes and sees her place)
1    0   The green man wakes and sees her place  The yellow man wakes and sees her place                                <NA>                             <NA>       llow         gr                                (diff_chg, llow)                               (diff_chg, gr)  (The , gr, e, en,  man wakes and sees her place)  (The , y, e, llow,  man wakes and sees her place)
2    0   The green man wakes and sees her place  The yellow man wakes and sees her place                                <NA>                             <NA>          y         en                                   (diff_chg, y)                               (diff_chg, en)  (The , gr, e, en,  man wakes and sees her place)  (The , y, e, llow,  man wakes and sees her place)
3    0   The green man wakes and sees her place  The yellow man wakes and sees her place                                <NA>                             <NA>       llow         en                                (diff_chg, llow)                               (diff_chg, en)  (The , gr, e, en,  man wakes and sees her place)  (The , y, e, llow,  man wakes and sees her place)
4    1            The spectacles upon her face;            The spectacles upon her face;                                <NA>                             <NA>       <NA>       <NA>                                             NaN                                          NaN                  (The spectacles upon her face;,)                   (The spectacles upon her face;,)
5    2                                                     The spectacles upon her face;       The spectacles upon her face;                             <NA>       <NA>       <NA>       (diff_add, The spectacles upon her face;)                                          NaN                                                ()                   (The spectacles upon her face;,)
6    3                                                     The spectacles upon her face;       The spectacles upon her face;                             <NA>       <NA>       <NA>       (diff_add, The spectacles upon her face;)                                          NaN                                                ()                   (The spectacles upon her face;,)
7    4         And now she's trying all she can   And now she is trying all that she can                                <NA>                             <NA>          i          '                                  (diff_chg,  i)                                (diff_chg, ')            (And now she, ', s trying all she can)   (And now she,  i, s trying all , that , she can)
8    4         And now she's trying all she can   And now she is trying all that she can                               that                              <NA>       <NA>          '                               (diff_add, that )                                (diff_chg, ')            (And now she, ', s trying all she can)   (And now she,  i, s trying all , that , she can)
9    5     To shoot the sleepy, green-coat man.      To shoot the tired, green-coat man.                                <NA>                             <NA>        tir         sl                                 (diff_chg, tir)                               (diff_chg, sl)    (To shoot the , sl, e, epy, , green-coat man.)      (To shoot the , tir, e, d, , green-coat man.)
10   5     To shoot the sleepy, green-coat man.      To shoot the tired, green-coat man.                                <NA>                             <NA>          d         sl                                   (diff_chg, d)                               (diff_chg, sl)    (To shoot the , sl, e, epy, , green-coat man.)      (To shoot the , tir, e, d, , green-coat man.)
11   5     To shoot the sleepy, green-coat man.      To shoot the tired, green-coat man.                                <NA>                             <NA>        tir        epy                                 (diff_chg, tir)                              (diff_chg, epy)    (To shoot the , sl, e, epy, , green-coat man.)      (To shoot the , tir, e, d, , green-coat man.)
12   5     To shoot the sleepy, green-coat man.      To shoot the tired, green-coat man.                                <NA>                             <NA>          d        epy                                   (diff_chg, d)                              (diff_chg, epy)    (To shoot the , sl, e, epy, , green-coat man.)      (To shoot the , tir, e, d, , green-coat man.)
13   6      He cries and screams and runs away;      He cries and screams and runs away;                                <NA>                             <NA>       <NA>       <NA>                                             NaN                                          NaN            (He cries and screams and runs away;,)             (He cries and screams and runs away;,)
14   7          The hare runs after him all day          The hare runs after him all day                                <NA>                             <NA>       <NA>       <NA>                                             NaN                                          NaN                (The hare runs after him all day,)                 (The hare runs after him all day,)
15   8          The hare runs after him all day       And hears him call out everywhere:  And hears him call out everywhere:  The hare runs after him all day       <NA>       <NA>  (diff_add, And hears him call out everywhere:)  (diff_sub, The hare runs after him all day)                (The hare runs after him all day,)              (And hears him call out everywhere:,)
16   9       And hears him call out everywhere:       And hears him call out everywhere:                                <NA>                             <NA>       <NA>       <NA>                                             NaN                                          NaN             (And hears him call out everywhere:,)              (And hears him call out everywhere:,)
17  10  "Help! Fire! Help! The Hare! The Hare!"  "Help! Fire! Help! The Hare! The Hare!"                                <NA>                             <NA>       <NA>       <NA>                                             NaN                                          NaN        ("Help! Fire! Help! The Hare! The Hare!",)         ("Help! Fire! Help! The Hare! The Hare!",)


"""

```

++--------------------------------------++
++--------------------------------------++
|| |)     . |   + .          +          ||
|| |+ | | | | +-+ | +-+ +-+ -+- +-+ +-+ ||
|| |) +-+ | | +-+ | | | +-+  +  +-+ | | ||
||                        |             ||
||                       -+             ||
||                      By RixTheTyrunt ||
++--------------------------------------++
++--------------------------------------++

You can use the [buildington.page] decorator and/or the [buildington.addFile] method to add a route to your website. Here's an example of both:
+------------------------------------------------------------------------------+
| Python                                                                       |
+------------------------------------------------------------------------------+
| import buildington                                                           |
|                                                                              |
| buildington.addFile("README.txt")                                            |
| @buildington.page("/")                                                       |
| def index():                                                                 |
|     return (                                                                 |
|         buildington.Para("Hippity hoppity your website is now my property"), |
|     )                                                                        |
|                                                                              |
| buildington.start("0.0.0.0", 8080)                                           |
+------------------------------------------------------------------------------+
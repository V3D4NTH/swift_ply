var some_var: Int = 555;
var glob: Int = some_function(some_var);
func some_function(a: Int) -> Int {
    a += 111;
    return a;
}

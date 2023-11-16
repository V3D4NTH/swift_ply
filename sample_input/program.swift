
func someOtherFunction(d: Int) -> Int{
    var b: Int = 20;
    if( 52 > 43){
        var f: Int = d;
        f = 20;
        b *= 32;
    }
    else {
        b *= 10;
    }
        return b;
}

func someOtherFunction2(a:Int) -> Int{
    for(var j: Int = 1; j < 21; j += 1;) {
        a = j + 5;
    }
    return a;
}
func someOtherFunction3(a:Int, b:Int) -> Int{
    for(var i: Int = 1; i < 20; i += 1;) {
        a += 1;
        b += 2;
    }
    return a;

}

func someComplexFunction(A: Int, B: Int, C: Int, D: Int)->Int {
    var someResult : Int = 42;
    for(var i: Int = 1; i < 3; i += 1;) {
        for(var j: Int = 1; j < 3; j += 1;) {
                 someResult += A * B - C - D + i + j;
                }
            }
    return someResult;
}


var a : Int = 0;

var b : Int = 0;
b = someOtherFunction(43);
a = someOtherFunction3(a,b);
a = someOtherFunction(52);
b = someComplexFunction(42,42,42,42);

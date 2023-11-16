var a : Int = 52;
func someOtherFunction(c: Int) -> Int{
    for(var j: Int = 0; j < 2; j+= 1;){
        c += 1;
    }
    return c;
}
a = someOtherFunction(a);
if( 100 < a) {
    repeat {
        a = a - 1;
    } while a > 50;
}
else {
    if(1 < a) {
        a *= 32;
        a = a > 43 ? a + 9 : a + 5;
    }
}


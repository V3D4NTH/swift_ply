var a : Int = 52;
func someOtherFunction(c: Int) -> Int{
    for(var j: Int = 0; j < 32*42; j+= 1;){
        c += 1;
    }
    return c;
}

a = someOtherFunction(a);

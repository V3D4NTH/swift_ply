func someOtherFunction(c: Int, a: Int, b: Int) -> Int {

    for(var j: Int = 0; j < 2; j+= 1;){
        c += 1;
    }
    if( a < 10 && b > 2){
        b = b / 32*21+a;
    }
    else{
        b += c;
    }
    if (c < 10){
        b += a;
    }
            return b;
}

var x: Int = someOtherFunction(1,2,3);
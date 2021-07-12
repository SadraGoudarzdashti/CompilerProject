package learnjava;

import testjava.Second;
import testjava.Fourth;

public class Third{
    public int p1;
    public int p2 = 20;
    private string name = "test";
    protected int p3 = 12;

     public void m1() {
        First obj1 = new First();
	    obj1.say("salam");

	    Second obj2 = new Second();
	    obj2.callme();

	    Fourth obj3 = new Fourth();
	    obj3.m2();

    }
}
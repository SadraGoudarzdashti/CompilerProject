package testjava;

import learnjava.*;

class Second {  
    private int pvfield;
    protected string protfield;

    public static void main(String[] args) {
        First obj = new First();
	    obj.msg();
	    obj.score = 12;
    	System.out.println(obj.score);
    }

    public void callme() {
        First obj = new First();
	    obj.msg();
	    obj.say("salam");
    }

    public int m1(){
        First obj1 = new First();
        Third obj2 = new obj2();
        obj1.score = 14;
        obj1.say("salaaam");
        return obj2.p2;
    }
}
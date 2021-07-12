package testjava;

import learnjava.*;

class Second {  
    private int pfield;
    public static void main(String[] args) {
        First obj = new First();
	    obj.msg();
	    obj.score = 12;
    	System.out.println(obj.score);
    }  
}
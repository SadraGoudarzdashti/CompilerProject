package testjava;


class Fourth {
    private int pfield;
    public static void main(String[] args) {
        learnjava.First obj = new learnjava.First();
	    obj.score = 14;
    	System.out.println(obj.score);
    }

    public void m1() {
        Second obj1 = new Second();
	    obj1.callme();
    }

     public void m2() {
        Second obj1 = new Second();
	    obj1.callme();

	    learnjava.Third obj2 = new learnjava.Third();
	    obj2.p1 = 16;
    }
}
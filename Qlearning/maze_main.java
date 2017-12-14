
public class maze_main {

	public static void main(String[] args) {
		QL_maze operator=new QL_maze((double)0.99,(double)0.05,(double)0.1);
		operator.Q_learning();
	}

}

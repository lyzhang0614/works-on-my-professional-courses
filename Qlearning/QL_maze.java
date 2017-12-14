import java.lang.Math;
import java.text.DecimalFormat;
public class QL_maze {
	Qvalue Qs_0[][]=new Qvalue[5][5];//5*5个状态及其4个Q值
	Qvalue Qs_old[][]=new Qvalue[5][5];//表示上一轮的所有状态动作对的Q值；
	Qvalue Qs_new[][]=new Qvalue[5][5];//表示这一轮的所有状态动作对的Q值；
	double discount;
	double rate;//learning rate
	double epsilon;//epsilon-greedy
	public QL_maze(double discount,double rate,double epsilon){
		init(Qs_old);
		init(Qs_new);
		this.discount=discount;
		this.rate=rate;
		this.epsilon=epsilon;
	}
	public void init(Qvalue Q[][]){//初始Q值为0
		for(int i=0;i<5;i++){
			for(int j=0;j<5;j++){
				Q[i][j]=new Qvalue();
			}
			
		}
	}
	public boolean isConvergent(){//判断迭代是否收敛
		double e=0;
		for(int i=0;i<5;i++){
			for(int j=0;j<5;j++){
				for(int k=0;k<4;k++){
					double newQ=Qs_new[i][j].Q[k];
					double oldQ=Qs_old[i][j].Q[k];
					e=e+Math.pow(newQ-oldQ,2);
				}
			}
		}	
		if(e<0.0001)
			return true;
		return false;
	}

	public void printQs(Qvalue Qs[][],int t){//打印Q值表
		System.out.println();
		for(int i=4;i>=0;i--){
			System.out.print(i+":");
			for(int j=0;j<5;j++){
				for(int a=0;a<4;a++){
					String k="";
					switch(a){
					case 0:
						k="↑";
						break;
					case 1:
						k="↓";
						break;
					case 2:
						k="←";
						break;
					case 3:
						k="→";
					}
					double Q=Qs[i][j].Q[a];
					DecimalFormat decimalFormat=new DecimalFormat("0.00");
					String p=decimalFormat.format(Q);
					System.out.print(k+p);
					if(a!=3)
						System.out.print(";");
				}
				System.out.print("      ");
			}
			System.out.println();
		}
		System.out.println(" \t\t 0:\t\t\t\t 1:\t\t\t\t 2:\t\t\t\t\t 3:\t\t\t\t 4:\t\t\t");
	}
	
	public int chooseAction(int i,int j){//epsilon-greedy算法选择动作
		int k;
		double p=Math.random();
		int a=Integer.valueOf((Qs_new[i][j].getMax().split(","))[1]);
		if(p>epsilon){
			k=a;
		}else{
			k=(int)(Math.random()*4);
		}
		switch(k){
		case 0:
			System.out.print("↑ ");
			break;
		case 1:
			System.out.print("↓ ");
			break;
		case 2:
			System.out.print("← ");
			break;
		case 3:
			System.out.print("→ ");
			break;
		}
		return k;
	}
	//==================核心算法：Q-Learning算法=========================//
	public void Q_learning(){
		int t=0; //迭代次数
		printQs(Qs_old,0);
		while(true){//尚未收敛时
			System.out.println(t+":");
			System.out.print("动作序列：");
			t++;
			int i=0;
			int j=0;
			while(i!=4||j!=4){
				
				//choose an action: epsilon-greedy
				int k;//选出的动作
				k=chooseAction(i,j);
				
				//确定惩罚值：
				int r=-1;
				int a=i;int b=j;//记录当前状态
				//get r and update the state:
				if(i==3&&j==4&&k==3 || i==4&&j==3&&k==0){//new state is the goal
					r=0;
					i=4;
					j=4;
				}else{
					switch(k){
						case 0://up
							if(j==4){
								r=-100;
							}else{
								j++;
							}
							break;
						case 1://down
							if(j==0){
								r=-100;
							}else{
								j--;
							}
							break;
						case 2://left
							if(i==0 || i==1&&(j==0||j==1) || i==2&&(j==3||j==4) || i==3&&(j==0||j==1)){
								r=-100;
							}else{
								i--;
							}
							break;
						case 3://right
							if(i==4 || i==0&&(j==0||j==1) || i==1&&(j==3||j==4) || i==2&&(j==0||j==1)){
								r=-100;
							}else{
								i++;
							}
					}
				}
				double currQ=Qs_new[a][b].Q[k];
				double nextQ=Double.parseDouble((Qs_new[i][j].getMax().split(","))[0]);
				Qs_new[a][b].Q[k]=(1-rate)*currQ+rate*(r+discount*nextQ);
			}
			
			printQs(Qs_new,t);
			
			if(isConvergent()) break;//直到收敛
			updateOld();
		}
		
	}
	
	public void updateOld(){
		for(int i=0;i<5;i++){
			for(int j=0;j<5;j++){
				for(int k=0;k<4;k++){
					Qs_old[i][j].Q[k]=Qs_new[i][j].Q[k];
				}
			}
		}
	}
}


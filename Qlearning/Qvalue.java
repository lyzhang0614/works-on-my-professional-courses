
public class Qvalue {
	double [] Q;
public Qvalue(){
	Q=new double[4];
	Q[0]=0;//s状态下向上移动的累计回报值
	Q[1]=0;//s状态下向下移动的累计回报值
	Q[2]=0;//s状态下向左移动的累计回报值
	Q[3]=0;//s状态下向右移动的累计回报值
}
public String getMax(){
	if(Q[0]==Q[1] && Q[2]==Q[1] && Q[2]==Q[3]){
		int a=(int)(Math.random()*4);
		return Q[0]+","+a;
	}
	double Qtemp=Q[0];
	int a=0;
	for(int i=1;i<4;i++){
		if(Q[i]>Qtemp){
			Qtemp=Q[i];
			a=i;
		}
	}
	return Qtemp+","+a;
}
}

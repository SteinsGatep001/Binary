#include<opencv2\opencv.hpp>
using namespace cv;
int main()
{
	Mat picture = imread("wallpaper.jpg");//图片必须添加到工程目录下
										  //也就是和test.cpp文件放在一个文件夹下！！！
	imshow("测试程序", picture);
	waitKey(20150901);
}
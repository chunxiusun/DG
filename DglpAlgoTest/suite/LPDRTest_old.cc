#include <iostream>
#include <fstream>
#include <string>
#include "../include/LPDR.hpp"
#include <stdlib.h>

#include "opencv/cv.h"
#include "opencv/highgui.h"

// Use for video 
#define DO_RECORDE 1

// Whether to show
#define BSHOW 0

// Add support for hainan (hai and kou)
#define LPDR_CLASS_NUM 79

#define TEST_NUM 1

#define THREAD_NUM 40


// Whether to enable watchdog
#define ENCRYPTED false

// Deal with in a sequence 
#define BATCH_SIZE 1

// Model bin file
#define LPDR_MDL "../bin/MDL/1102_2"

// Car color we support
const char *paColors[6] = {"UNKNOWN", "BLUE", "YELLOW", "WHITE", "BLACK", "GREEN"};

// Car plate number we support
const char *paInv_chardict2[LPDR_CLASS_NUM] = {"_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", \
        "A", "B", "C", "D", "E", "F", "G", "H", "J", \
        "K", "L", "M", "N", "P", "Q", "R", "S", "T",\
        "U", "V", "W", "X", "Y", "Z", "I", "京", "津",\
        "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", \
        "皖", "闽", "鲁", "新", "苏", "浙", "赣", "鄂", \
        "桂", "甘", "晋", "蒙", "陕", "吉", "贵", "粤", \
        "青", "藏", "川", "宁", "琼", "使", "领", "试", \
        "学", "临", "时", "警", "港", "O", "挂", "澳","#"
                                              };

int ipl2bin(IplImage *pimg, mx_float *pfBuffer, mx_uint bufflen);

int test_imglist(string &fname, string errfile, string resultfile);

//注意：当字符串为空时，也会返回一个空字符串
void split(string& s, string& delim, vector<string> *ret);

int main(int argc, char* argv[])
{

    string fname(argv[1]);
    cout << fname << endl;

    string errfile = "../testResult/err.list";
    string resultfile = "../testResult/result.list";

    test_imglist(fname, errfile, resultfile);

    cout << "bye bye ..." << endl;

    return 0;
}

//{{{ test_imglist
int test_imglist(string &fname, string errfile, string resultfile)
{
    FILE *pf = fopen(fname.c_str(), "r");

    if (!pf)
    {
        printf("cannot open file.\n");
        return -1;
    }

    LPDR_OutputSet_S stOutput;
    LPDR_HANDLE hLPDRHandle = 0;


    float fZoom = 1.0f;
    int zeronum = 0;

    CvFont font1;
    cvInitFont(&font1, CV_FONT_HERSHEY_SIMPLEX, 0.47, 0.47, 0, 1, 8);

    dgLP::LPDR *pclsLPDR = new dgLP::LPDR(LPDR_MDL, 0, ENCRYPTED, 0, 0);

    float costtime, diff;
    struct timeval start2, end2, start, end;

    ifstream infile;
    ofstream outfile, outresult;

    string strfilename;
    string previousLine="";


    char filename[256];
    char abyText[256];
    string strSplit = " ";
    int num = 0;
    int errnum = 0;
    int realnum = 0;
    int dwImgH = 0, dwImgW = 0;
    int dwImgH2 = 0, dwImgW2 = 0;

    if (BSHOW)
    {
        cv::namedWindow("hello_rgb", cv::WINDOW_NORMAL);
    }
    cv::Mat imgcolor;
    uchar *pubyImgData = 0;
    vector<string> strparts;

    LPDR_ImageSet_S stImgSet;

    stImgSet.dwImageNum = BATCH_SIZE;

    infile.open(fname);

    if (errfile != "")
    {
        outfile.open(errfile);
    }

    if (resultfile != "")
    {
        outresult.open(resultfile);
    }
    float fAllCost = 0.f;
    int dwDoNumber =0;
    int dwAllLPCount = 0;
    int dwRightLPCount = 0;
    int dwRecallCount = 0;
    int dwHasNum = 0;
    while (1)
    {
        getline(infile, strfilename);
        if (infile.eof()) break;
        cout << endl;
        cout << strfilename << endl;
        split(strfilename, strSplit, &strparts);

        cv::Mat imgcolor_ori = cv::imread(strparts[0], CV_LOAD_IMAGE_COLOR);
        if (imgcolor_ori.rows == 0)
        {
            printf("no more pictures ...\n");
            continue;
        }

        num++;
        printf("frame: %d\n", num);

        if (num<1) continue;
        dwAllLPCount += strparts.size() - 1;

        if (1)
        {
            dwImgH2 = imgcolor_ori.rows;
            dwImgW2 = imgcolor_ori.cols;

            cv::resize(imgcolor_ori, imgcolor, cv::Size(dwImgW2*fZoom, dwImgH2*fZoom), 0, 0, CV_INTER_LINEAR);
            dwImgH = imgcolor.rows;
            dwImgW = imgcolor.cols;

            if (0)
            {
                cv::Mat borderImg(dwImgH+20, dwImgW+20, CV_8UC3);
                cv::copyMakeBorder(imgcolor, borderImg, 0, 20, 0, 20, cv::BORDER_CONSTANT, 0);
                cv::imshow("fuck", borderImg);
                cv::waitKey(0);
            }
        }

        uchar *pubyData = (uchar*)imgcolor.data;

        for (int dwBI = 0; dwBI < BATCH_SIZE; dwBI++)
        {
            stImgSet.astSet[dwBI].pubyData = pubyData;
            stImgSet.astSet[dwBI].dwImgW = dwImgW;
            stImgSet.astSet[dwBI].dwImgH = dwImgH;
        }

        gettimeofday(&start, NULL);
        for (int kk = 0; kk < TEST_NUM; kk++)
        {
            gettimeofday(&start2, NULL);
            pclsLPDR->Process(&stImgSet, &stOutput);

            gettimeofday(&end2, NULL);
            diff = ((end2.tv_sec-start2.tv_sec)*1000000+ end2.tv_usec-start2.tv_usec) / 1000.f;
            fAllCost += diff;
            dwDoNumber ++;
            cout << kk << ":" << diff << endl;
        }
        gettimeofday(&end, NULL);
        diff = ((end.tv_sec-start.tv_sec)*1000000+ end.tv_usec-start.tv_usec) / 1000.f;
        printf("LPDR_Process cost:%.2fms\n", diff/TEST_NUM);

        char key;
        int dwWait = 10;
        int dwSave = 0;
        int dwMargin;
        cv::Mat images[8] = {imgcolor, imgcolor, imgcolor, imgcolor, imgcolor, imgcolor, imgcolor, imgcolor};

        int dwNowRightCount = 0;

        for (int dwI = 0; dwI < stOutput.dwImageNum; dwI++)
        {
            cout << "image:" << dwI << endl;
            LPDR_Output_S *pstOut = stOutput.astLPSet + dwI;
            cv::Mat &imgnow = images[dwI];
            string strallinfo = "";
            for (int dwJ = 0; dwJ < pstOut->dwLPNum; dwJ++)
            {
                dwHasNum++;
                LPDRInfo_S *pstLP = pstOut->astLPs + dwJ;
                int *pdwLPRect = pstLP->adwLPRect;
                dwMargin = (pdwLPRect[3] - pdwLPRect[1])/4;
                int dwX0 = pdwLPRect[0] - dwMargin;
                int dwY0 = pdwLPRect[1] - dwMargin;
                int dwX1 = pdwLPRect[2] + dwMargin;
                int dwY1 = pdwLPRect[3] + dwMargin;

                if (BSHOW)
                {
                    cv::rectangle(imgnow, cv::Point(dwX0, dwY0), cv::Point(dwX1, dwY1), CV_RGB(255, 0, 0), 2, 8, 0);
                }
                string text = "";
                for (int dwK = 0; dwK < pstLP->dwLPLen; dwK++)
                {
                    cout << paInv_chardict2[pstLP->adwLPNumber[dwK]];
                    text += paInv_chardict2[pstLP->adwLPNumber[dwK]];
                }

                cout << endl;

                for (int dwK = 0; dwK < pstLP->dwLPLen; dwK++)
                {
                    cout << setprecision(6) << pstLP->afScores[dwK] << ",";
                }

                cout << endl;

                stringstream sspos;
                string strpos;
                //sspos << dwX0 << "," << dwY0 << "," << dwX1 << "," << dwY1 << ";";
                sspos << dwX0 << "," << dwY0 << "," << dwX1 << "," << dwY1 << " ";
                sspos >> strpos;
                //strallinfo += " " + strpos + text;
                //strallinfo += " " + text  + " " + strpos;
                strallinfo += " " + text;
                if (BSHOW)
                {
                    CvFont fontB = cv::fontQt("Times", 20, cv::Scalar(255, 0, 0));
                    if (pstLP->dwColor==LP_COLOUR_YELLOW)
                    {
                        cv::rectangle(imgnow, cv::Point(dwX0, dwY0-25), cv::Point(dwX0+140, dwY0), CV_RGB(200, 200, 0), CV_FILLED);
                    }
                    else if (pstLP->dwColor==LP_COLOUR_WHITE)
                    {
                        cv::rectangle(imgnow, cv::Point(dwX0, dwY0-25), cv::Point(dwX0+140, dwY0), CV_RGB(200, 200, 200), CV_FILLED);
                    }
                    else if (pstLP->dwColor==LP_COLOUR_BLUE)
                    {
                        cv::rectangle(imgnow, cv::Point(dwX0, dwY0-25), cv::Point(dwX0+140, dwY0), CV_RGB(0, 0, 200), CV_FILLED);
                    }
                    cv::addText(imgnow, text, cv::Point(dwX0, dwY0-4), fontB);
                }

                bool bRight = false;
                for (int mi = 1; mi < strparts.size(); mi++)
                {
                    string platenow = strparts[mi];
                    string recogplate = "";
                    for (int dwK = 0; dwK < pstLP->dwLPLen; dwK++)
                    {
                        recogplate += paInv_chardict2[pstLP->adwLPNumber[dwK]];
                    }


                    int dwCmp = platenow.compare(recogplate);
                    if (dwCmp == 0)
                    {
                        bRight = true;
                        break;
                    }
                }

                cout << " " << pstLP->fAllScore << ", type:" << pstLP->dwType << ", color:" << paColors[pstLP->dwColor];
                if (pstLP->dwColor==LP_COLOUR_WHITE)
                {
                }
                if (bRight)
                {
                    dwRightLPCount++;
                    dwNowRightCount++;
                    cout << "--------Right!";
                }
                cout << endl;
            }

            if (resultfile != "")
            {
                //outresult << strfilename << strallinfo << endl;
                outresult << strparts[0] << strallinfo << endl;
            }

            if (errfile != "")
            {
                if (dwNowRightCount != strparts.size() - 1)
                {
                    outfile << strfilename << endl;
                }
            }
            printf("========>>Right_Ratio: %.2f%%[%d/%d/%d]\n", dwRightLPCount*100.0f/dwAllLPCount, dwRightLPCount, dwHasNum, dwAllLPCount);
            printf("[avg_cost: %0.2f ms] \n", fAllCost/dwDoNumber);
            if (BSHOW)
            {
                char abyName[128];
                sprintf(abyName, "/home/mingzhang/Pictures/special/%d.jpg", num);
                cv::imshow("hello_rgb", imgnow);
                if (dwSave)
                {
                    cv::imwrite(abyName, imgcolor_ori);
                }
                dwWait = 0;
                key = cv::waitKey(dwWait);
            }
        }

        if (key == 'c' || key == 'C')
        {
            break;
        }
        else if (key == ' ')
        {
            cv::waitKey(0);
        }
    }

    infile.close();

    if (errfile != "")
    {
        outfile.close();
    }

    if (resultfile != "")
    {
        outresult.close();
    }

    delete pclsLPDR;
    pclsLPDR = 0;

    return 0;
}
//}}}


int ipl2bin(IplImage *pimg, mx_float *pfBuffer, mx_uint bufflen)
{
    int width = pimg->width;
    int height = pimg->height;
    int wstep = pimg->widthStep;
    int imgsz = width * height;
    unsigned char *data = (unsigned char*)pimg->imageData;

    assert(imgsz <= bufflen);

    for (int ri = 0; ri < height; ri++)
    {
        for (int ci = 0; ci < width; ci++)
        {
            pfBuffer[ri * width + ci] = data[ri * wstep + ci] / 255.f;
        }
    }

    return 0;
}


//注意：当字符串为空时，也会返回一个空字符串
void split(string& s, string& delim, vector<string> *ret)
{
    size_t last = 0;
    size_t index=s.find_first_of(delim,last);
    ret->clear();
    while (index!=string::npos)
    {
        ret->push_back(s.substr(last,index-last));
        last=index+1;
        index=s.find_first_of(delim,last);
    }
    if (index-last>0)
    {
        ret->push_back(s.substr(last,index-last));
    }
}

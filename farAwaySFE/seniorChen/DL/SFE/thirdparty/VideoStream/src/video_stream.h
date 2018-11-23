#pragma once
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <iostream>
#include <HCNetSDK.h>
#include <PlayM4.h>
#include "threadsafe_queue.h"

using namespace std;
using namespace cv;

namespace sfe
{
LONG uid = -1;
LONG play_handle = -1;
LONG play_port = -1;
threadsafe_queue<Mat> mat_queue;
LONG frame_width = -1;
LONG frame_height = -1;

#if defined(WIN32)
void CALLBACK DecCallBack(long nPort, char *pBuf, long nSize, FRAME_INFO *pFrameInfo, void *nReserved1, void *nReserved2)
#else
void CALLBACK DecCallBack(LONG nPort, char *pBuf, LONG nSize, FRAME_INFO *pFrameInfo, void *nReserved1, LONG nReserved2)
#endif
{
	if (pBuf == NULL)
		return;
	if (frame_width == -1 || frame_height == -1)
	{
		frame_width = pFrameInfo->nWidth;
		frame_height = pFrameInfo->nHeight;
	}
	Mat dst(pFrameInfo->nHeight, pFrameInfo->nWidth, CV_8UC3);
	Mat src(pFrameInfo->nHeight + pFrameInfo->nHeight / 2, pFrameInfo->nWidth, CV_8UC1, (uchar *)pBuf);
	cvtColor(src, dst, CV_YUV2BGR_YV12);
	mat_queue.push(dst);
}

void CALLBACK g_RealDataCallBack_V30(LONG lRealHandle, DWORD dwDataType, BYTE *pBuffer, DWORD dwBufSize, void *dwUser)
{
	switch (dwDataType)
	{
	case NET_DVR_SYSHEAD:				 //系统头
		if (!PlayM4_GetPort(&play_port)) //获取播放库未使用的通道号
			break;
		if (dwBufSize > 0)
		{
			if (!PlayM4_SetStreamOpenMode(play_port, STREAME_REALTIME)) //设置实时流播放模式
				break;
			if (!PlayM4_OpenStream(play_port, pBuffer, dwBufSize, SOURCE_BUF_MAX)) //打开流接口
				break;
			if (!PlayM4_SetDecCallBack(play_port, DecCallBack)) //设置解码回调
				break;

			if (!PlayM4_Play(play_port, NULL)) //播放开始
				break;
		}
		break;
	case NET_DVR_STREAMDATA: //码流数据
		if (dwBufSize > 0 && play_port != -1)
			if (!PlayM4_InputData(play_port, pBuffer, dwBufSize))
				break;
		break;
	default: //其他数据
		if (dwBufSize > 0 && play_port != -1)
			if (!PlayM4_InputData(play_port, pBuffer, dwBufSize))
				break;
		break;
	}
}

void CALLBACK g_ExceptionCallBack(DWORD dwType, LONG lUserID, LONG lHandle, void *pUser)
{
	char tempbuf[256] = {0};
	switch (dwType)
	{
	case EXCEPTION_RECONNECT: //预览时重连
		printf("----------reconnect--------\n");
		break;
	default:
		break;
	}
}

bool init(char *ip, int port, char *user, char *pwd, int channel)
{
	if (uid >= 0)
		return false;
	//---------------------------------------
	// 初始化
	NET_DVR_Init();
	//设置连接时间与重连时间
	NET_DVR_SetConnectTime(2000, 10);
	NET_DVR_SetReconnect(10000, true);

	//---------------------------------------
	// 注册设备
	NET_DVR_DEVICEINFO_V30 struDeviceInfo;
	uid = NET_DVR_Login_V30(ip, port, user, pwd, &struDeviceInfo);
	if (uid < 0)
	{
		printf("Login error, %d\n", NET_DVR_GetLastError());
		NET_DVR_Cleanup();
		return false;
	}

	//---------------------------------------
	//设置异常消息回调函数
	NET_DVR_SetExceptionCallBack_V30(0, NULL, g_ExceptionCallBack, NULL);

	//---------------------------------------
	//启动预览并设置回调数据流
	NET_DVR_PREVIEWINFO struPlayInfo = {0};
	struPlayInfo.hPlayWnd = NULL;									   //需要SDK解码时句柄设为有效值，仅取流不解码时可设为空
	struPlayInfo.lChannel = struDeviceInfo.byStartDChan + channel - 1; //预览通道号
	struPlayInfo.dwStreamType = 0;									   //0-主码流，1-子码流，2-码流3，3-码流4，以此类推
	struPlayInfo.dwLinkMode = 0;									   //0- TCP方式，1- UDP方式，2- 多播方式，3- RTP方式，4-RTP/RTSP，5-RSTP/HTTP

	play_handle = NET_DVR_RealPlay_V40(uid, &struPlayInfo, g_RealDataCallBack_V30, NULL);
	if (play_handle < 0)
	{
		printf("NET_DVR_RealPlay_V40 error, %d\n", NET_DVR_GetLastError());
		NET_DVR_Logout(uid);
		NET_DVR_Cleanup();
		return false;
	}

	return true;
}

void destroy()
{
	frame_width = frame_height = -1;

	//关闭预览
	if (play_handle >= 0)
	{
		NET_DVR_StopRealPlay(play_handle);
		play_handle = -1;
	}

	//释放播放库资源
	if (play_port >= 0)
	{
		PlayM4_Stop(play_port);
		PlayM4_CloseStream(play_port);
		PlayM4_FreePort(play_port);
		play_port = -1;
	}

	//注销用户
	if (uid >= 0)
	{
		NET_DVR_Logout(uid);
		NET_DVR_Cleanup();
		uid = -1;
	}

	while (!mat_queue.empty())
		mat_queue.wait_and_pop();
}

shared_ptr<Mat> next_frame()
{
	if (uid < 0)
		return NULL;
	return mat_queue.wait_and_pop();
}
}
/*******************************************************************************
 * Copyright (c) 2014 IBM Corp.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution.
 *
 * The Eclipse Public License is available at
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *   http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *    Ian Craggs - initial API and implementation and/or initial documentation
 *    Sergio R. Caprile - clarifications and/or documentation extension
 *******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cmsis_os2.h"
#include "ohos_init.h"

#include "MQTTClient.h"
#include "wifi_sta_connect.h"

#include "cJSON.h"



static unsigned char sendBuf[1000];
static unsigned char readBuf[1000];

// #define WIFI_SSID "wyPhone"
// #define WIFI_PWD "lab203534"
#define WIFI_SSID "jjj"
#define WIFI_PWD "88888888"

#define HOST_ADDR "123.60.210.214"

#define Device_Id "fa69b0cd-6bb8-8d35-087c-f823397b25e2"

#define PUBLISH_TOPIC "device/attributes"
#define SUBCRIB_TOPIC "device/attributes/"Device_Id
#define RESPONSE_TOPIC "$oc/devices/"Device_Id"/sys/commands/response" ///request_id={request_id}"


Network network;
MQTTClient client;
osThreadId_t thread_id;
/*
电机开关标识符
*/
int motorsw=0;
/*
电机发送数据
*/
void motorSend(int motorSwitch,int motorSpeed){
        MQTTMessage message;
        char payload[300]={0};
        char *publishtopic=PUBLISH_TOPIC;
        cJSON *root = cJSON_CreateObject();
        if(root != NULL){
            //温湿度的cJSON数据
            cJSON_AddNumberToObject(root,"switch",motorSwitch);
            cJSON_AddNumberToObject(root,"speed",motorSpeed);
            char *palyload_str=cJSON_PrintUnformatted(root);
            //放入整理好的负载
            strcpy(payload,palyload_str);

            cJSON_free(palyload_str);
            cJSON_Delete(root);
        }
        message.qos = 2;
        message.retained = 0;
        message.payload = payload;
        message.payloadlen = strlen(payload);

        printf("Return code from MQTT publish is %d\n", MQTTPublish(&client, publishtopic, &message));
}

void messageArrived(MessageData* data)
{      
     
 int rc;
    cJSON *root = cJSON_ParseWithLength( data->message->payload, data->message->payloadlen);
    if(root != NULL){
        cJSON *sw = cJSON_GetObjectItem(root,"switch");
        cJSON *sd = cJSON_GetObjectItem(root,"speed");
        if(sw!= NULL){
            int ms = cJSON_GetNumberValue(sw);
                        if(ms== 1){    
                            hi_pwm_start(2,200,65535);     
                            motorsw=1;
                            motorSend(1,200);
                        }    
                           
                        else if(ms== 0){
                            motor_speed(0);
                            // hi_pwm_start(MOTOR_PWM_CHN, , 65535);
                            motorSend(0,0);
                            motorsw=0;
                        }   
                 }
        if (motorsw==1&&sd!=NULL){
            int f=cJSON_GetNumberValue(sd);
            if(f==0){  
                motor_speed(0);
            }
            // 类型转化
            printf("电机转速 %d",f);
            // motor_speed(f);
            hi_pwm_start(2,f,65535);
            motorSend(1,f);
        }
        cJSON_Delete(root);
    }

        
}


static void MQTTDemoTask(void)
{
    motor_init();
    initI2C();

    //初始化sht30
    InitSHT30();

    printf(">> MQTTDemoTask ...\n");
    /*连接wifi*/
    WifiConnect(WIFI_SSID, WIFI_PWD);
    printf("Starting ...\n");
    int rc, count = 0;

    /*网络初始化*/
    NetworkInit(&network);
    printf("NetworkConnect  ...\n");

begin:
    /* 连接网络*/
    NetworkConnect(&network, HOST_ADDR, 1883);
    printf("MQTTClientInit  ...\n");
    printf("我猜他没到达这里！！！");
    /*MQTT客户端初始化*/
    MQTTClientInit(&client, &network, 2000, sendBuf, sizeof(sendBuf), readBuf, sizeof(readBuf));

    MQTTString clientId = MQTTString_initializer;
    clientId.cstring = Device_Id;

    MQTTString userName = MQTTString_initializer;
    userName.cstring = Device_Id;

    MQTTString password = MQTTString_initializer;
    password.cstring = "";

    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
    data.clientID = clientId;

    data.username = userName;
	data.password = password;

    data.willFlag = 0;
    data.MQTTVersion = 4;
    data.keepAliveInterval = 60;
    data.cleansession = 1;

/*led屏显示*/


test_led_screen();
    //连接MQTT代理
    printf("MQTTConnect  ...\n");
    rc = MQTTConnect(&client, &data);
    if (rc != 0) {
        printf("MQTTConnect: %d\n", rc);
        NetworkDisconnect(&network);
        MQTTDisconnect(&client);
        osDelay(200);
        goto begin;
    }

    // printf("MQTTSubscribe  ...\n");
    //订阅者
    printf("进行MQTT订阅....\n");
    rc = MQTTSubscribe(&client, SUBCRIB_TOPIC, 2, messageArrived);
    printf("已经执行完MQTT的订阅者步骤！！！\n");

    if (rc != 0) {
        printf("MQTTSubscribe: %d\n", rc);
        osDelay(200);
        goto begin;
    }
    /*
    
    电机初始化，防止上线开启
    */
    motorSend(0,0);


    while (++count) {
        float temp;
        float humi;

        // SHT3X_ReadMeasurementBuffer(&temp,&humi);

        MQTTMessage message;
        char *publishtopic=PUBLISH_TOPIC;

        char payload[300]={0};

        cJSON *root = cJSON_CreateObject();

        extern float g_temp;
        extern float g_humi;

        if(root != NULL){

            
            //温湿度的cJSON数据
            cJSON_AddNumberToObject(root,"humidity",g_humi);
            cJSON_AddNumberToObject(root,"temperature",g_temp);
            char *palyload_str=cJSON_PrintUnformatted(root);
            //放入整理好的负载
            strcpy(payload,palyload_str);

            cJSON_free(palyload_str);
            cJSON_Delete(root);
        }
     
        message.qos = 0;
        message.retained = 0;
        message.payload = payload;
        // sprintf(payload, "{\"services\": [  \
        //     {\"service_id\": \"fan_serv\",  \"properties\": {\"temprature\": %02f,\"humidity\": %02f } \
        //     }   \
        //     ]}", g_temp,g_humi);
        message.payloadlen = strlen(payload);
        //MQTT话题发布者
        if ((rc = MQTTPublish(&client, publishtopic, &message)) != 0) {
            printf("Return code from MQTT publish is %d\n", rc);
            NetworkDisconnect(&network);
            MQTTDisconnect(&client);
            goto begin;
        }else{
            printf("mqtt publish success:%s\n",payload);
        }
        /*阻塞至多5000ms,有消息下发则退出阻塞*/
        MQTTYield(&client, 500);
        // osDelay(500);
    }
}    

static void MQTTDemo(void)
{
    // oled_gpio_io_init();
    osThreadAttr_t attr;

    attr.name = "MQTTDemoTask";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = 10240;
    attr.priority = osPriorityNormal;

    if (osThreadNew((osThreadFunc_t)MQTTDemoTask, NULL, &attr) == NULL) {
        printf("[MQTT_Demo] Failed to create MQTTDemoTask!\n");
    }
}

APP_FEATURE_INIT(MQTTDemo);
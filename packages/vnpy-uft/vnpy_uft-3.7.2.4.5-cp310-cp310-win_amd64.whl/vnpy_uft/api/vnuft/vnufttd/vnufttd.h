//ϵͳ
#ifdef WIN32
#include "pch.h"
#endif

#include "vnuft.h"
#include "pybind11/pybind11.h"
#include "uft/HSTradeApi.h"


using namespace pybind11;

//����
#define ONFRONTCONNECTED 0
#define ONFRONTDISCONNECTED 1
#define ONRSPAUTHENTICATE 2
#define ONRSPSUBMITUSERSYSTEMINFO 3
#define ONRSPUSERLOGIN 4
#define ONRSPUSERPASSWORDUPDATE 5
#define ONRSPERRORORDERINSERT 6
#define ONRSPORDERACTION 7
#define ONRSPERROREXERCISEORDERINSERT 8
#define ONRSPEXERCISEORDERACTION 9
#define ONRSPERRORLOCKINSERT 10
#define ONRSPFORQUOTEINSERT 11
#define ONRSPERRORCOMBACTIONINSERT 12
#define ONRSPQUERYMAXORDERVOLUME 13
#define ONRSPQRYLOCKVOLUME 14
#define ONRSPQUERYEXERCISEVOLUME 15
#define ONRSPQRYCOMBVOLUME 16
#define ONRSPQRYPOSITION 17
#define ONRSPQRYTRADINGACCOUNT 18
#define ONRSPQRYORDER 19
#define ONRSPQRYTRADE 20
#define ONRSPQRYEXERCISE 21
#define ONRSPQRYLOCK 22
#define ONRSPQRYCOMBACTION 23
#define ONRSPQRYPOSITIONCOMBINEDETAIL 24
#define ONRSPQRYINSTRUMENT 25
#define ONRSPQRYCOVEREDSHORT 26
#define ONRSPQRYEXERCISEASSIGN 27
#define ONRSPTRANSFER 28
#define ONRSPQRYTRANSFER 29
#define ONRSPQUERYBANKBALANCE 30
#define ONRSPQUERYBANKACCOUNT 31
#define ONRSPMULTICENTREFUNDTRANS 32
#define ONRSPQUERYBILLCONTENT 33
#define ONRSPBILLCONFIRM 34
#define ONRSPQRYMARGIN 35
#define ONRSPQRYCOMMISSION 36
#define ONRSPQRYPOSITIONDETAIL 37
#define ONRSPQRYEXCHANGERATE 38
#define ONRSPQRYSYSCONFIG 39
#define ONRSPQRYDEPTHMARKETDATA 40
#define ONRSPFUNDTRANS 41
#define ONRSPQRYFUNDTRANS 42
#define ONRSPQRYCLIENTNOTICE 43
#define ONRSPQRYOPTUNDERLY 44
#define ONRSPQRYSECUDEPTHMARKET 45
#define ONRSPQRYHISTORDER 46
#define ONRSPQRYHISTTRADE 47
#define ONRTNTRADE 48
#define ONRTNORDER 49
#define ONRTNEXERCISE 50
#define ONRTNCOMBACTION 51
#define ONRTNLOCK 52
#define ONERRRTNORDERACTION 53
#define ONRTNCLIENTNOTICE 54


///-------------------------------------------------------------------------------------
///C++ SPI�Ļص���������ʵ��
///-------------------------------------------------------------------------------------

//API�ļ̳�ʵ��
class TdApi : public CHSTradeSpi
{
private:
	CHSTradeApi* api;                     //API����
    thread task_thread;                    //�����߳�ָ�루��python���������ݣ�
    TaskQueue task_queue;                //�������
    bool active = false;                //����״̬

public:
    TdApi()
    {
    };

    ~TdApi()
    {
        if (this->active)
        {
            this->exit();
        }
    };

    //-------------------------------------------------------------------------------------
    //API�ص�����
    //-------------------------------------------------------------------------------------

	/// Description: ���ͻ����뽻�׺�̨��ʼ����ͨ�����ӣ����ӳɹ���˷������ص���
	virtual void OnFrontConnected();

	/// Description:���ͻ����뽻�׺�̨ͨ�������쳣ʱ���÷��������á�
	/// Others     :ͨ��GetApiErrorMsg(nResult)��ȡ��ϸ������Ϣ��
	virtual void OnFrontDisconnected(int nResult);

	/// Description:�ͻ���֤
	virtual void OnRspAuthenticate(CHSRspAuthenticateField *pRspAuthenticate, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ն���Ϣ�ϱ��ӿ�(�м�ģʽ)
	virtual void OnRspSubmitUserSystemInfo(CHSRspUserSystemInfoField *pRspUserSystemInfo, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ͻ���¼
	virtual void OnRspUserLogin(CHSRspUserLoginField *pRspUserLogin, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�������
	virtual void OnRspUserPasswordUpdate(CHSRspUserPasswordUpdateField *pRspUserPasswordUpdate, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����¼��
	/// Others     :��������˷������ص���pRspOrderInsert����������ʱ����Ľṹ�����ݡ�
	virtual void OnRspErrorOrderInsert(CHSRspOrderInsertField *pRspOrderInsert, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����
	virtual void OnRspOrderAction(CHSRspOrderActionField *pRspOrderAction, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Ȩ¼��
	/// Others     :��Ȩ¼�����˷������ص���pRspExerciseOrderInsert����������ʱ����Ľṹ�����ݡ�
	virtual void OnRspErrorExerciseOrderInsert(CHSRspExerciseOrderInsertField *pRspExerciseOrderInsert, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Ȩ����
	virtual void OnRspExerciseOrderAction(CHSRspExerciseOrderActionField *pRspExerciseOrderAction, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����¼��
	/// Others     :��������˷������ص���pRspExerciseOrderAction����������ʱ����Ľṹ�����ݡ�
	virtual void OnRspErrorLockInsert(CHSRspLockInsertField *pRspExerciseOrderAction, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:ѯ��¼��
	virtual void OnRspForQuoteInsert(CHSRspForQuoteInsertField *pRspForQuoteInsert, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�������¼��
	virtual void OnRspErrorCombActionInsert(CHSRspCombActionInsertField *pRspCombActionInsert, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��󱨵�������ȡ
	virtual void OnRspQueryMaxOrderVolume(CHSRspQueryMaxOrderVolumeField *pRspQueryMaxOrderVolume, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:������������ȡ
	virtual void OnRspQryLockVolume(CHSRspQryLockVolumeField *pRspQryLockVolume, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����Ȩ������ȡ
	virtual void OnRspQueryExerciseVolume(CHSRspQueryExerciseVolumeField *pRspQueryExerciseVolume, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����������������ȡ
	virtual void OnRspQryCombVolume(CHSRspQryCombVolumeField *pRspQryCombVolume, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ֲֲ�ѯ
	virtual void OnRspQryPosition(CHSRspQryPositionField *pRspQryPosition, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ʽ��˻���ѯ
	virtual void OnRspQryTradingAccount(CHSRspQryTradingAccountField *pRspQryTradingAccount, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:������ѯ
	virtual void OnRspQryOrder(CHSOrderField *pRspQryOrder, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ɽ���ѯ
	virtual void OnRspQryTrade(CHSTradeField *pRspQryTrade, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Ȩ��ѯ
	virtual void OnRspQryExercise(CHSExerciseField *pRspQryExercise, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:������ѯ
	virtual void OnRspQryLock(CHSLockField *pRspQryLock, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:������ϲ�ѯ
	virtual void OnRspQryCombAction(CHSCombActionField *pRspQryCombAction, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��ϳֲ���ϸ��ѯ
	virtual void OnRspQryPositionCombineDetail(CHSRspQryPositionCombineDetailField *pRspQryPositionCombineDetail, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Լ��Ϣ��ѯ
	virtual void OnRspQryInstrument(CHSRspQryInstrumentField *pRspQryInstrument, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����ȱ�ڲ�ѯ
	virtual void OnRspQryCoveredShort(CHSRspQryCoveredShortField *pRspQryCoveredShort, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Ȩָ�ɲ�ѯ
	virtual void OnRspQryExerciseAssign(CHSRspQryExerciseAssignField *pRspQryExerciseAssign, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����ת��
	virtual void OnRspTransfer(CHSRspTransferField *pRspTransfer, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:����ת�˲�ѯ
	virtual void OnRspQryTransfer(CHSRspQryTransferField *pRspQryTransfer, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��������ѯ
	virtual void OnRspQueryBankBalance(CHSRspQueryBankBalanceField *pRspQueryBankBalance, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�����˻���ѯ
	virtual void OnRspQueryBankAccount(CHSRspQueryBankAccountField *pRspQueryBankAccount, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�������ʽ����
	virtual void OnRspMultiCentreFundTrans(CHSRspMultiCentreFundTransField *pRspMultiCentreFundTransfer, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ͻ��˵���ѯ
	virtual void OnRspQueryBillContent(CHSRspQueryBillContentField *pRspQueryBillContent, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ͻ��˵�ȷ��
	virtual void OnRspBillConfirm(CHSRspBillConfirmField *pRspBillConfirm, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��֤���ѯ
	virtual void OnRspQryMargin(CHSRspQryMarginField *pRspQryMargin, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�����Ѳ�ѯ
	virtual void OnRspQryCommission(CHSRspQryCommissionField *pRspQryCommission, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ֲ���ϸ��ѯ
	virtual void OnRspQryPositionDetail(CHSRspQryPositionDetailField *pRspQryPositionDetail, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:���ʲ�ѯ
	virtual void OnRspQryExchangeRate(CHSRspQryExchangeRateField *pRspQryExchangeRate, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:���͹�˾���ò�����ѯ
	virtual void OnRspQrySysConfig(CHSRspQrySysConfigField *pRspQrySysConfig, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�����ѯ
	virtual void OnRspQryDepthMarketData(CHSDepthMarketDataField *pRspQryDepthMarketData, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ʽ����
	virtual void OnRspFundTrans(CHSRspFundTransField *pRspFundTransfer, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:�ʽ������ˮ��ѯ
	virtual void OnRspQryFundTrans(CHSRspQryFundTransField *pRspQryFundTrans, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��ѯ�ͻ�֪ͨ
	virtual void OnRspQryClientNotice(CHSClientNoticeField *pRspQryClientNotice, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��Ȩ�����Ϣ��ѯ
	virtual void OnRspQryOptUnderly(CHSRspQryOptUnderlyField *pRspQryOptUnderly, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:֤ȯ�����ѯ
	virtual void OnRspQrySecuDepthMarket(CHSRspQrySecuDepthMarketField *pRspQrySecuDepthMarket, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��ʷ������ѯ
	virtual void OnRspQryHistOrder(CHSOrderField *pRspQryHistOrder, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description:��ʷ�ɽ���ѯ
	virtual void OnRspQryHistTrade(CHSTradeField *pRspQryHistTrade, CHSRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	/// Description: ����-�ɽ��ر�
	virtual void OnRtnTrade(CHSTradeField *pRtnTrade);

	/// Description: ����-�����ر�
	virtual void OnRtnOrder(CHSOrderField *pRtnOrder);

	/// Description: ����-��Ȩ
	virtual void OnRtnExercise(CHSExerciseField *pRtnExercise);

	/// Description: ����-�������
	virtual void OnRtnCombAction(CHSCombActionField *pRtnCombAction);

	/// Description: ����-����
	virtual void OnRtnLock(CHSLockField *pRtnLock);

	/// Description: ����-��������ر�
	virtual void OnErrRtnOrderAction(CHSOrderActionField *pRtnOrder);

	/// Description: ����-�ͻ�֪ͨ
	virtual void OnRtnClientNotice(CHSClientNoticeField *pRtnClientNotice);

    //-------------------------------------------------------------------------------------
    //task������
    //-------------------------------------------------------------------------------------
    void processTask();

	void processFrontConnected(Task *task);

	void processFrontDisconnected(Task *task);

	void processRspAuthenticate(Task *task);

	void processRspSubmitUserSystemInfo(Task *task);

	void processRspUserLogin(Task *task);

	void processRspUserPasswordUpdate(Task *task);

	void processRspErrorOrderInsert(Task *task);

	void processRspOrderAction(Task *task);

	void processRspErrorExerciseOrderInsert(Task *task);

	void processRspExerciseOrderAction(Task *task);

	void processRspErrorLockInsert(Task *task);

	void processRspForQuoteInsert(Task *task);

	void processRspErrorCombActionInsert(Task *task);

	void processRspQueryMaxOrderVolume(Task *task);

	void processRspQryLockVolume(Task *task);

	void processRspQueryExerciseVolume(Task *task);

	void processRspQryCombVolume(Task *task);

	void processRspQryPosition(Task *task);

	void processRspQryTradingAccount(Task *task);

	void processRspQryOrder(Task *task);

	void processRspQryTrade(Task *task);

	void processRspQryExercise(Task *task);

	void processRspQryLock(Task *task);

	void processRspQryCombAction(Task *task);

	void processRspQryPositionCombineDetail(Task *task);

	void processRspQryInstrument(Task *task);

	void processRspQryCoveredShort(Task *task);

	void processRspQryExerciseAssign(Task *task);

	void processRspTransfer(Task *task);

	void processRspQryTransfer(Task *task);

	void processRspQueryBankBalance(Task *task);

	void processRspQueryBankAccount(Task *task);

	void processRspMultiCentreFundTrans(Task *task);

	void processRspQueryBillContent(Task *task);

	void processRspBillConfirm(Task *task);

	void processRspQryMargin(Task *task);

	void processRspQryCommission(Task *task);

	void processRspQryPositionDetail(Task *task);

	void processRspQryExchangeRate(Task *task);

	void processRspQrySysConfig(Task *task);

	void processRspQryDepthMarketData(Task *task);

	void processRspFundTrans(Task *task);

	void processRspQryFundTrans(Task *task);

	void processRspQryClientNotice(Task *task);

	void processRspQryOptUnderly(Task *task);

	void processRspQrySecuDepthMarket(Task *task);

	void processRspQryHistOrder(Task *task);

	void processRspQryHistTrade(Task *task);

	void processRtnTrade(Task *task);

	void processRtnOrder(Task *task);

	void processRtnExercise(Task *task);

	void processRtnCombAction(Task *task);

	void processRtnLock(Task *task);

	void processErrRtnOrderAction(Task *task);

	void processRtnClientNotice(Task *task);

    //-------------------------------------------------------------------------------------
    //data���ص������������ֵ�
    //error���ص������Ĵ����ֵ�
    //id������id
    //last���Ƿ�Ϊ��󷵻�
    //i������
    //-------------------------------------------------------------------------------------    

	virtual void onFrontConnected() {};

	virtual void onFrontDisconnected(int reqid) {};

	virtual void onRspAuthenticate(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspSubmitUserSystemInfo(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspUserLogin(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspUserPasswordUpdate(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspErrorOrderInsert(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspOrderAction(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspErrorExerciseOrderInsert(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspExerciseOrderAction(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspErrorLockInsert(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspForQuoteInsert(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspErrorCombActionInsert(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQueryMaxOrderVolume(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryLockVolume(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQueryExerciseVolume(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryCombVolume(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryPosition(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryTradingAccount(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryOrder(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryTrade(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryExercise(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryLock(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryCombAction(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryPositionCombineDetail(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryInstrument(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryCoveredShort(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryExerciseAssign(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspTransfer(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryTransfer(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQueryBankBalance(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQueryBankAccount(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspMultiCentreFundTrans(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQueryBillContent(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspBillConfirm(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryMargin(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryCommission(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryPositionDetail(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryExchangeRate(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQrySysConfig(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryDepthMarketData(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspFundTrans(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryFundTrans(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryClientNotice(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryOptUnderly(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQrySecuDepthMarket(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryHistOrder(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRspQryHistTrade(const dict &data, const dict &error, int reqid, bool last) {};

	virtual void onRtnTrade(const dict &data) {};

	virtual void onRtnOrder(const dict &data) {};

	virtual void onRtnExercise(const dict &data) {};

	virtual void onRtnCombAction(const dict &data) {};

	virtual void onRtnLock(const dict &data) {};

	virtual void onErrRtnOrderAction(const dict &data) {};

	virtual void onRtnClientNotice(const dict &data) {};

    //-------------------------------------------------------------------------------------
    //req:���������������ֵ�
    //-------------------------------------------------------------------------------------

	void newTradeApi(string pszFlowPath);

    int init(string pszLicFile, string pszSafeLevel, string pszPwd, string pszSslFile, string pszSslPwd);

    int join();

	int exit();

	int rgisterSubModel(int eSubType);

	int registerFront(string pszFrontAddress);

	int registerFensServer(string pszFensAddress, string pszAccountID);

	string getApiErrorMsg(int nErrorCode);

	int getTradingDate();

	int reqAuthenticate(const dict &req, int reqid);

	int reqSubmitUserSystemInfo(const dict &req, int reqid);

	int reqUserLogin(const dict &req, int reqid);

	int reqUserPasswordUpdate(const dict &req, int reqid);

	int reqOrderInsert(const dict &req, int reqid);

	int reqOrderAction(const dict &req, int reqid);

	int reqExerciseOrderInsert(const dict &req, int reqid);

	int reqExerciseOrderAction(const dict &req, int reqid);

	int reqLockInsert(const dict &req, int reqid);

	int reqForQuoteInsert(const dict &req, int reqid);

	int reqCombActionInsert(const dict &req, int reqid);

	int reqQueryMaxOrderVolume(const dict &req, int reqid);

	int reqQryLockVolume(const dict &req, int reqid);

	int reqQueryExerciseVolume(const dict &req, int reqid);

	int reqQryCombVolume(const dict &req, int reqid);

	int reqQryPosition(const dict &req, int reqid);

	int reqQryTradingAccount(const dict &req, int reqid);

	int reqQryOrder(const dict &req, int reqid);

	int reqQryTrade(const dict &req, int reqid);

	int reqQryExercise(const dict &req, int reqid);

	int reqQryLock(const dict &req, int reqid);

	int reqQryCombAction(const dict &req, int reqid);

	int reqQryPositionCombineDetail(const dict &req, int reqid);

	int reqQryInstrument(const dict &req, int reqid);

	int reqQryCoveredShort(const dict &req, int reqid);

	int reqQryExerciseAssign(const dict &req, int reqid);

	int reqTransfer(const dict &req, int reqid);

	int reqQryTransfer(const dict &req, int reqid);

	int reqQueryBankBalance(const dict &req, int reqid);

	int reqQueryBankAccount(const dict &req, int reqid);

	int reqMultiCentreFundTrans(const dict &req, int reqid);

	int reqQueryBillContent(const dict &req, int reqid);

	int reqBillConfirm(const dict &req, int reqid);

	int reqQryMargin(const dict &req, int reqid);

	int reqQryCommission(const dict &req, int reqid);

	int reqQryExchangeRate(const dict &req, int reqid);

	int reqQryPositionDetail(const dict &req, int reqid);

	int reqQrySysConfig(const dict &req, int reqid);

	int reqQryDepthMarketData(const dict &req, int reqid);

	int reqFundTrans(const dict &req, int reqid);

	int reqQryFundTrans(const dict &req, int reqid);

	int reqQryClientNotice(const dict &req, int reqid);

	int reqQryOptUnderly(const dict &req, int reqid);

	int reqQrySecuDepthMarket(const dict &req, int reqid);

	int reqQryHistOrder(const dict &req, int reqid);

	int reqQryHistTrade(const dict &req, int reqid);
};

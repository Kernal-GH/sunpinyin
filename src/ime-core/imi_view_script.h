#ifndef SUNPY_IMI_SCRIPT_VIEW_H
#define SUNPY_IMI_SCRIPT_VIEW_H

#include "portability.h"

#include "imi_view.h"
#include "python_plugin.h"

class CIMIScriptableView : public CIMIView 
{
public:
    CIMIScriptableView();
    virtual ~CIMIScriptableView();

    virtual void attachIC(CIMIContext* pIC);
    virtual unsigned clearIC(void);

    virtual bool onKeyEvent(const CKeyEvent&);

    virtual void updateWindows(unsigned mask);

    virtual void getPreeditString(IPreeditString& ps);
    virtual void getCandidateList(ICandidateList& cl, int start, int size);

    virtual int  onCandidatePageRequest(int pgno, bool relative);
    virtual int  onCandidateSelectRequest(int index);

private:
    unsigned    m_cursorFrIdx;
    unsigned    m_candiFrIdx;
    unsigned    m_candiPageFirst;

    bool        m_numeric_mode;

    CCandidates m_candiList;
    wstring     m_tailSentence;

    static PyPlugins m_plugins;

    inline void _insert (unsigned keyvalue, unsigned& mask);
    inline void _erase (bool backward, unsigned& mask);

    inline void _getCandidates ();
    inline void _makeSelection (int candiIdx, unsigned& mask);
    inline void _deleteCandidate (int candiIdx, unsigned& mask);

    inline void _commitChar (TWCHAR ch);
    inline void _commitString (const wstring& wstr);
    inline void _doCommit (bool bConvert=true);

    inline unsigned _moveLeft (unsigned& mask, bool searchAgain=true);
    inline unsigned _moveLeftSyllable (unsigned& mask, bool searchAgain=true);
    inline unsigned _moveHome (unsigned& mask, bool searchAgain=true);

    inline unsigned _moveRight (unsigned& mask);
    inline unsigned _moveRightSyllable (unsigned& mask);
    inline unsigned _moveEnd (unsigned& mask);

    inline wstring _plugin_trans(const wstring& str);
};

#endif

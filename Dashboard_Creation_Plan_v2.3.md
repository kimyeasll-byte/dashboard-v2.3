# Dashboard Creation Plan v2.3 (Final Edition)

## 0. Project Overview
- **버전:** v2.3 (v2.4 피드백 반영 및 최종 통합본)
- **목표:** '인사기획 및 전산팀'의 모든 업무(회계, PMO, 자산, 리서치)를 전산화하는 완전한 Local Storage 기반 하이브리드 대시보드 구축.
- **주요 특징:** 서버나 DB 구축 전이라도 브라우저 Local Storage를 통해 모든 데이터가 영구 보존(Cumulative)되며, 실시간 시장 데이터 연동(KOSPI, 개별 종목, 환점, 반도체 가격)을 통해 구매 및 재무 전략의 가시성을 극대화함.

---

## 1. UI/UX Design Strategy (Minimalist White)
- **테마:** 화이트 배경(#FFFFFF) + 딥블랙 텍스트(#1A1A1A) + 미니멀 보더 라인.
- **레이아웃 구성:** Single Page Application (SPA), 반응형 Grid 형태의 카드 모듈.
- **상세 스타일:**
  - 글로벌 헤더 우측에 시장 지표 배너 영역 마련.
  - 모든 테이블(Table)은 끈적한(Sticky) 헤더를 가지며 hover 반응.
  - Sticky Notes(스마트 메모) 영역 도입.

---

## 2. Core Feature Specifications

### ① Global Market & ESG Intelligence (실시간 연동)
- **주가 및 시장 지표 (상단 헤더):** 
  - KOSPI 지수 실시간 시뮬레이팅 반영 (전일비 갱신 포함).
  - 파워넷(037030) 주가 실시간 표시.
  - **리프레시:** 1시간 단위(3600초) 자동 갱신.
- **Chart.js 시장 동향:** [차세대 메모리 지수 (미달러 USD 기준표기)] 라인 차트 표기.
- **AI 비품 구매 전략:** AI 인프라 확대로 단기적 가격 인상 예고에 따른 비품 예산 편성 권고 배너 영역 추가.
- **ESG 뉴스 피드:** 3시간(10800초) 주기로 임의의 ESG 관련 뉴스 헤드라인 전환 및 외부 하이퍼링크(a태그) 연동.

### ② Finance Automation (회계 지출결의)
- **가시성 강화:** 하단 테이블 '비율(사:연)' 컬럼에 "52% (배분금액) / 48% (배분금액)" 형식으로 원화 금액 자동 계산 후 병기 출력. `calcSplit()` 로직 반영.
- **누적 및 필터링:**
  - 지출결의 내역을 시간 역순으로 Local Storage 영구 누적.
  - 테이블 상단의 **[연도] 및 [월] 드롭다운** 필터를 통해 특정 월의 내역만 빠르게 필터링 조회가 가능하며, 동기화된 해당 필터 구간의 총 지출 합계 금액('sumFilteredExp')이 즉시 렌더링.
- **입력:** 품의일자, 사용처(내역명), 총액(KRW), 사업부/연구소 부담 비율 분기, 정기결제 여부.

### ③ Asset Inventory History (자산 수불 대장)
- **최신 데이터 자동 강조 로직 (중요):**
  - 자산 및 비품 수불 이력의 가장 직관적인 모니터링을 위해 **모든 개별 품목(Name) 기준, 가장 최근에 발생한(Date 기준) ROW에만 '연한 노란색 음영'을 주고 명칭 앞에 파란색 커스텀 마커(★)를 표기**하여 즉시 잔여수량 확인이 가능함.
- **컬럼 직관화:** 최종 재고량을 '재고' 컬럼으로 명칭 변경.
- **이전 재고(Base) 자동 로드:** 
  - 새로운 품명 입력 폼에 이전에 등록했던 랩탑이나 데스크탑 등 이름을 기입(Key Input)할 시, **해당 이름으로 쌓인 히스토리 중 가장 최근의 '재고'(curr) 값을 찾아 '기초 재고(Base)' 칸에 자동 세팅**해줌. 이로써 불필요한 기초 재고 수동 타이핑 감소.

### ④ PMO Pipeline & Minutes (프로젝트 태스크 트래커)
- **과제 추적:** 프로젝트별 목표, 진척률(0~100%), 상태(대기/진행/완료) 누적.
- **Modal Minutes (상세 로그):** 과제명을 클릭 시 해당 과제로만 필터링 된 실무 Task 및 회의록(Minutes) 타임라인을 모달 창으로 조회하고 기록 가능하게 구성.

### ⑤ Smart Sticky Notes (스마트 메모장)
- **구분 관리:** 메모 저장 시 '메모 제목(Title)'과 '상세 내용(Content)'을 시각적으로 구분하여 렌더링.
- **포스트잇 레이아웃:** CSS Grid 기반으로 작성 시 노란색 카드 UI가 자동으로 배열되며 생성 및 즉시 삭제 가능.

---

## 3. Data Schema & Persistence (Local Storage Hybrid)
서버 통신 이전에, 브라우저 스토리지 체계에 기반하여 완벽한 Zero-Downtime 데이터를 구축합니다. JSON.stringify를 통해 저장됩니다.
- **저장 변수명:** `DASHBOARD_V2_FINAL_COMPLETE`

```javascript
let state = {
  expenses: {  
    "exp_1700000000000": { date, name, total, bizRatio, rndRatio, bizAmt, rndAmt, isAuto } 
  },
  inventoryHistory: {  
    "invLog_1700000000123": { date, name, memo, base, inS, outS, curr } 
  },
  projects: {  
    "prj_1700000000555": { name, status, progress } 
  },
  tasks: {  
    "tsk_1700000000777": { prjId, type, content, time } 
  },
  memos: {  
    "memo_1700000000999": { date, title, content } 
  }
}
```

## 4. Deployment Strategy
- 본 Dashboard는 `index.html` 단일 파일 SPA 구조로 설계/운영됩니다.
- 모든 스크립트 모듈(Chart.js CDN 포함) 및 인라인 CSS가 index.html 에 포함되어 있어 즉시 실행 및 검증 기능을 내포합니다.

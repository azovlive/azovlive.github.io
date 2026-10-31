# 🖼️ [작업 표준 가이드] 웹 성능 극대화를 위한 이미지 관리 및 최적화 규격
## Web Image Management & Performance Optimization Guidelines

본 문서는 UWILL 공식 홈페이지 및 GitHub Pages 배포 시 웹사이트 로딩 속도 단축, Core Web Vitals(LCP/CLS) 최적화, 모바일 데이터 절약을 위해 수립된 **이미지 자산 관리 및 최적화 표준 작업 규격**입니다.

---

## 1. 핵심 원칙: 원본(Master)과 배포본(Production)의 분리

깃허브 배포 디렉토리(`GitHubSite_Upload/public`)에 수 메가바이트(MB)에 달하는 원본 고해상도 이미지가 직접 업로드되는 것을 방지하기 위해, 저장 공간을 엄격히 이원화하여 관리합니다.

```text
[UwillHomePage_automation] (프로젝트 루트)
 ├── Doc/images/master/                 <-- 📂 [원본 보관소] 고해상도 무손실 마스터 에셋 보관
 │    ├── Newlogo-2.png (1287x1287, 907KB)
 │    ├── Newlogo.png (1.95MB)
 │    └── screenshots/ (앱 원본 스크린샷)
 │
 └── GitHubSite_Upload/public/          <-- 🚀 [배포용 보관소] 화면 규격에 맞춰 압축된 에셋만 배치
      ├── Newlogo-2.webp (256x256, 14.6KB - 98.4% 감축)
      ├── Newlogo-2.png  (256x256, 54.2KB - 호환용)
      └── assets/
```

1. **프로젝트 원본 이미지**:
   - 위치: `Doc/images/master/`
   - 목적: 원본 디자인 소스(PSD, AI, 고해상도 무손실 PNG) 보존
   - 주의: 해당 디렉토리의 파일은 빌드 및 배포 대상에 포함되지 않음.

2. **배포용 최적화 이미지**:
   - 위치: `GitHubSite_Upload/public/`
   - 목적: 웹 브라우저의 실제 화면 표시 규격에 맞게 리사이징 및 압축된 경량 에셋 서빙.

---

## 2. 웹 표시 요소별 최대 규격 및 용량 상한선 기준표

웹 브라우저에서 표시되는 CSS 크기(`Display Size`)와 모바일/데스크톱 고해상도 화면(Retina 2x~3x)을 고려한 최대 허용 규격 기준입니다.

| 구분 | 화면 표시 크기 | 고해상도 고려 최대 해상도 | 권장 포맷 | 목표 파일 용량 | 주요 적용 위치 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **브랜드 로고 / 심볼** | `36px ~ 72px` | **`256 × 256 px`** | `WebP` (PNG 대체) | **< 20 KB** (최대 30KB) | 헤더, 푸터, 히어로 엠블럼 |
| **파비콘 / 앱 터치 아이콘** | `32px ~ 180px` | **`256 × 256 px`** | `WebP` / `PNG` / `ICO` | **< 30 KB** | 브라우저 탭, 모바일 북마크 |
| **앱 아이콘 (라인업)** | `64px ~ 96px` | **`256 × 256 px`** | `WebP` (PNG 대체) | **< 30 KB** | 앱 목록, 카드 컴포넌트 |
| **앱 스크린샷 / 카드** | `300px ~ 480px`| **`800 × 1000 px`** (가로 최대) | `WebP` | **< 80 KB** (최대 120KB) | 앱 상세, 쇼케이스 갤러리 |
| **히어로 배경 / 배너** | `1200px+` | **`1200 × 1600 px`** (가로 최대) | `WebP` | **< 150 KB** (최대 200KB) | 상단 배너, 배경 그래픽 |
| **단색 UI 아이콘 / 심볼**| `16px ~ 24px` | **벡터 (무한 해상도)** | `SVG` | **< 5 KB** | 버튼 아이콘, 네비게이션 |

---

## 3. 포맷 및 압축 가이드라인

1. **차세대 포맷 WebP 기본 적용**:
   - 모든 래스터(비트맵) 이미지는 기본적으로 `.webp` 포맷으로 변환하여 사용합니다.
   - 품질(Quality) 설정: `90 ~ 95` (시각적 손실 없이 원본 대비 80~98% 용량 감축).
   - 다운샘플링 필터: `LANCZOS` 알고리즘을 사용하여 축소 시에도 디테일과 텍스트의 선명도를 유지합니다.

2. **레거시/메타데이터 호환용 PNG 병행**:
   - Open Graph (`og:image`), 레거시 파비콘, 또는 WebP를 지원하지 않는 외부 크롤러를 위해 동급으로 최적화된 `.png` 파일을 함께 보관합니다.

3. **아이콘류는 SVG 활용**:
   - 단색 아이콘, 심볼, 기하학적 도형은 래스터 이미지 대신 `SVG` 또는 CSS 기반 아이콘(Material Symbols 등)을 사용합니다.

---

## 4. 프론트엔드 마크업(Astro / HTML) 작성 규칙

이미지 로딩으로 인한 사용자 경험 저하 및 누적 레이아웃 이동(CLS)을 방지하기 위해 다음 규칙을 반드시 준수합니다.

```html
<!-- 1. 헤더 / 푸터 로고 (CLS 방지를 위해 width, height 명시) -->
<img src="/Newlogo-2.webp" alt="UWILL Logo" class="brand-logo" width="36" height="36" />

<!-- 2. 히어로 대표 이미지 (LCP 성능 최적화: 높은 우선순위 부여) -->
<img src="/Newlogo-2.webp" alt="UWILL Logo" class="hero-logo-img" width="72" height="72" fetchpriority="high" />

<!-- 3. 본문 및 하단 스크린샷 (스크롤 도달 시 비동기 지연 로딩) -->
<img src="/assets/screenshots/app.webp" alt="App Screenshot" width="800" height="600" loading="lazy" decoding="async" />
```

---

## 5. 원클릭 이미지 최적화 스크립트 사용법

향후 신규 이미지 자산 추가 시 간편하게 규격에 맞춰 변환할 수 있도록 전용 스크립트가 제공됩니다.

### 실행 위치: 프로젝트 루트
```bash
# 기본 사용법: 256px 상한 리사이징 및 WebP/PNG 동시 생성
python scripts/optimize_image.py <원본이미지경로> -o <출력디렉토리>

# 예시 1: 마스터 로고를 배포용 public 디렉토리로 최적화 복사 (256px)
python scripts/optimize_image.py Doc/images/master/Newlogo-2.png -o GitHubSite_Upload/public/ -s 256

# 예시 2: 앱 스크린샷 최적화 (가로 최대 800px, WebP 품질 90)
python scripts/optimize_image.py Doc/images/master/screenshot1.png -o GitHubSite_Upload/public/assets/ -s 800 -q 90
```

### 옵션 안내
- `-s, --max-size`: 이미지의 가로/세로 중 긴 쪽의 최대 픽셀 상한선 (기본값: `256`)
- `-q, --quality`: WebP 압축 품질 (기본값: `92`, 권장범위: `85~95`)
- `-o, --output`: 최적화된 파일이 저장될 출력 디렉토리 (기본값: 입력 파일 경로와 동일)
- `--no-png`: PNG 대체 파일 없이 WebP 파일만 단독 생성할 때 사용

---

## 6. 배포 전 체크리스트 (Gate Verification)

GitHub에 변경 사항을 커밋/푸시하기 전 반드시 다음 항목을 확인합니다:
- [ ] `GitHubSite_Upload/public/`에 500KB를 초과하는 고용량 이미지가 없는가?
- [ ] 웹 화면에 직접 렌더링되는 모든 이미지가 `.webp` 또는 `.svg` 포맷으로 지정되어 있는가?
- [ ] 모든 `<img>` 태그에 `width` 및 `height` 속성이 명시되어 있는가?
- [ ] 원본 고해상도 마스터 파일은 `Doc/images/master/`에 보관되어 있는가?

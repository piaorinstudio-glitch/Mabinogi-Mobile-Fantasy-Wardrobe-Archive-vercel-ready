// 2026-09-17 KR wardrobe update.
// Loaded after data/catalog.js and data/pets.js, before assets/js/app.js.
(() => {
  window.MABI = window.MABI || {};
  const data = Array.isArray(window.MABI.DATA) ? window.MABI.DATA : (window.MABI.DATA = []);

  // The new pass / lucky boxes become the current entries.
  for (const item of data) {
    if (item && (item.type === 'pass' || item.type === 'lucky')) item.latest = false;
  }

  const updates = [
    {
      id: 'pass-13',
      type: 'pass',
      typeLabel: '冒險家通行證',
      number: 13,
      zh: '柔和豐收',
      ko: '마일드 하베스트',
      lines: ['柔和豐收', '마일드 하베스트'],
      date: '2026-09-17',
      endDate: '2026-10-29',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545050',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/42bd81a4-abb1-4de4-bfc6-ea9fba2ffc23/%EB%AA%A8%ED%97%98%EA%B0%80%ED%8C%A8%EC%8A%A4%EA%B2%8C%EC%8B%9C%EB%AC%BC%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png',
      image: 'image/pass-13.png',
      latest: true
    },
    {
      id: 'lucky-37',
      type: 'lucky',
      typeLabel: '幸運箱',
      number: 37,
      zh: '克勞德・萊米（音譯）',
      ko: '클라우드 래미',
      lines: ['克勞德・萊米（音譯）', '클라우드 래미', '套裝｜Cloud Rammy', '클라우드 래미'],
      date: '2026-09-17',
      endDate: '2026-10-15',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545054',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/65bf6c16-9ba6-44b9-82eb-2cc0f16aacb7/%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%EB%9E%98%EB%AF%B8%ED%8C%A8%EC%85%98%EB%9F%AD%ED%82%A4%EB%B0%95%EC%8A%A4%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png',
      image: 'image/lucky-37.png',
      latest: true
    },
    {
      id: 'lucky-38',
      type: 'lucky',
      typeLabel: '幸運箱',
      number: 38,
      zh: '路森特・奧斯（音譯）',
      ko: '루센트 오스',
      lines: ['路森特・奧斯（音譯）', '루센트 오스', '套裝｜Lucent Oath', '루센트 오스'],
      date: '2026-09-17',
      endDate: '2026-10-15',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545054',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/3b9f6fff-1e65-49cc-a895-9e77ee9ea298/%EB%A3%A8%EC%84%BC%ED%8A%B8%EC%98%A4%EC%8A%A4%ED%8C%A8%EC%85%98%EB%9F%AD%ED%82%A4%EB%B0%95%EC%8A%A4%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png',
      image: 'image/lucky-38.png',
      latest: true
    },
    {
      id: 'package-7',
      type: 'package',
      typeLabel: '全套套組',
      number: 7,
      zh: '盛大合奏',
      ko: '그랜드 앙상블',
      lines: ['盛大合奏', '그랜드 앙상블'],
      date: '2026-09-17',
      endDate: '2026-12-17',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545055',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/c6e12ff5-645e-4736-b1b9-8879859a33ec/%ED%86%A0%ED%83%88%ED%8C%A8%ED%82%A4%EC%A7%80%EA%B2%8C%EC%8B%9C%EB%AC%BC%EC%9D%B4%EB%AF%B8%EC%A7%80900x750B.png',
      image: 'image/package-7.png'
    },
    {
      id: 'legend-7',
      type: 'legend',
      typeLabel: '傳說時裝',
      number: 7,
      zh: '哈維斯提亞・布雷辛（音譯）',
      ko: '하베스티아 블레싱',
      lines: ['哈維斯提亞・布雷辛（音譯）', '하베스티아 블레싱', '一般版', '長袍版'],
      date: '2026-09-17',
      endDate: '2026-12-17',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545058',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260917/693fc379-8b1e-4d02-b3d4-294477c66576/%ED%95%98%EB%B2%A0%EC%8A%A4%ED%8B%B0%EC%95%84%EB%B8%94%EB%A0%88%EC%8B%B1%EC%95%A1%ED%84%B0.png',
      image: 'image/legend-7.png',
      regularImage: 'image/legend-7.png',
      hoodedImage: 'image/legend-7-robe.png',
      imageMode: 'regular'
    },
    {
      id: 'pet-20',
      type: 'pet',
      typeLabel: '寵物',
      number: 20,
      zh: '英國牧羊犬系列',
      ko: '잉글리시 쉽독',
      lines: ['英國牧羊犬系列', '잉글리시 쉽독'],
      kind: '常規',
      date: '2026-09-17',
      endDate: '2026-11-05',
      year: '2026',
      notice: 'https://mabinogimobile.nexon.com/News/Notice/3545053',
      sourceImage: 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/9864aedd-648e-41a3-9d9e-74e5103a9859/%EC%9E%89%EA%B8%80%EB%A6%AC%EC%8B%9C%EC%89%BD%EB%8F%85%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png',
      image: 'image/pet-20.png',
      variants: [
        {zh: '慶典英國牧羊犬', ko: '페스티벌 잉글리시 쉽독', rarity: '史詩'},
        {zh: '圍巾英國牧羊犬', ko: '스카프 잉글리시 쉽독', rarity: '菁英'},
        {zh: '緞帶英國牧羊犬', ko: '리본 잉글리시 쉽독', rarity: '稀有'},
        {zh: '灰色英國牧羊犬', ko: '회색 잉글리시 쉽독', rarity: '高級'}
      ],
      imageNote: ''
    }
  ];

  const byId = new Map(data.map((item, index) => [item.id, index]));
  for (const item of updates) {
    const index = byId.get(item.id);
    if (index === undefined) {
      data.push(item);
      byId.set(item.id, data.length - 1);
    } else {
      data[index] = {...data[index], ...item};
    }
  }
})();

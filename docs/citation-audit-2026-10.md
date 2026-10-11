# Citation Audit — 2026-10-11

> A repository-wide check of whether the legal and standards instruments cited
> across `packs/` and `docs/` are still in force, and whether any **article-level
> citations** have gone stale.
>
> Triggered by discovering that 《中华人民共和国网络安全法》was amended on
> 2025-10-28 and **renumbered**. Scope: CN legal instruments and GB standards
> actually cited by this repository. International instruments (GDPR, HIPAA,
> ISO, NIST, HL7, DICOM, SNOMED, TFMEA, Incoterms, …) were **not** re-verified
> in this pass — see "What this audit did not cover".

## 1. Method and its limits

- Every `regulatory:` id used across the 17 pack manifests was extracted (47
  distinct ids) and grouped by instrument.
- Every **article-level** citation in the repository was located by pattern
  (`法》第X条`). There are **4 in total**, all added in the current content
  work; none predate it.
- Each CN instrument below was checked against an **official** source
  (中国政府网 / 中国人大网 / 全国标准信息公共服务平台) rather than secondary
  commentary, wherever an official page was reachable.

**Honest limit of this pass:** the official standards platform
(`openstd.samr.gov.cn`) returns HTTP 200 for a **search** URL whether or not
the standard number exists. A 200 there proves reachability, **not existence**.
Standard existence was therefore confirmed via search results showing the
standard's title and status, never by URL probing alone. This distinction is
recorded because it is exactly the trap that produced a fabricated ISO
citation in `packs/data-ai/lakehouse-platform` earlier.

## 2. Findings

### 2.1 ❌ CORRECTION REQUIRED — 《网络安全法》 renumbered

| | |
|---|---|
| Instrument | 《中华人民共和国网络安全法》 |
| Amendment | 主席令第六十一号, passed 2025-10-28 by the 18th session of the 14th NPC Standing Committee |
| Effective | **2026-01-01** |
| Key effect | "《中华人民共和国网络安全法》根据本决定作相应修改并**对条文顺序作相应调整，重新公布**" |
| Worked example | Graded-protection duties: **Article 21** (pre-2026) → **Article 23** (current) |
| Official text | <http://www.npc.gov.cn/c2/c30834/202510/t20251028_449048.html> (verified 200) |

**Blast radius.** No pre-existing article-level citation of this law was found —
the repository named the law but never cited an article. The exposure is
therefore to *future* citations and to any reader who looks up an article number
from an older source. `packs/healthcare/his-emr` already carries an explicit
warning (added in PR #16); this audit propagates the note to the remaining
pack that names the law.

### 2.2 ❌ GAP NOW CLOSED — 《电子印章管理办法》 exists

| | |
|---|---|
| Instrument | 《电子印章管理办法》 |
| Citation | **国办发〔2025〕33号**, State Council General Office |
| Dates | Signed 2025-09-27, published 2025-10-09 |
| Status | **第三十八条: effective on promulgation** |
| Official text | <https://www.gov.cn/zhengce/content/202510/content_7043696.htm> (full text retrieved) |

Both `workflow-bpm` and `one-stop-service` had recorded an open question of the
form *"the mandate for a national unified electronic seal system names no
technical standard, so the pack names none"*. That question was **partly
answerable already** and is now answered. Load-bearing provisions:

- **第五条** — a compliant 电子印章 has the same legal effect as a physical
  seal; a sealed electronic file has the same effect as a paper one with a
  physical seal.
- **第十六条** — the seal's e-signature certificate must be valid and issued by
  a lawfully established e-certification body; the **seal's expiry must not
  exceed its certificate's**; the data format, generation process and
  **application interface** must conform to national standards.
- **第十七条** — the seal production/filing body **must provide a seal status
  query service**. This is a concrete integration requirement a platform must
  design for.
- **第二十一条** — the principle **"谁所有、谁控制，谁签章、谁负责"**.
- **第二十二条** — sealing process information must be **recorded and retained**,
  making the seal action traceable and attributable.
- **第二十三条** — verification must check not only authenticity/integrity/
  non-repudiation but **whether the seal was valid at the time of signing** —
  a distinct check from verifying it now.
- **第二十七条** — business systems of administrative organs and public-service
  bodies **shall support compliant electronic seals**. This is a *mandate*, and
  it strengthens `one-stop-service`'s dependency argument beyond the basis
  previously available.

### 2.3 ✅ CONFIRMED CURRENT — GB/T 22239-2019 (MLPS 2.0)

Official platform shows **现行**, published 2019-05-10, effective 2019-12-01.
The `mlps-2-0` id used in **11 manifests** is accurate. The wider MLPS family
(GB/T 22240-2020, GB/T 25058-2019, GB/T 25070-2019, GB/T 28448-2019) is also
现行.

### 2.4 ⚠️ FORTHCOMING — GB/T 36959-2026

**GB/T 36959-2026《网络安全技术 网络安全等级保护测评机构能力要求和评估规范》**
— published 2026-05-25, **effective 2026-12-01**, superseding GB/T 36959-2018.

Not a citation error today, but any pack describing the assessment regime
should note the change. **Affected:** anything relying on graded-protection
assessment.

### 2.5 ✅ CONFIRMED CURRENT — 《电子签名法》

Still the **2019 second amendment** (2004 enacted; amended 2015-04-24 and
2019-04-23). The Articles 13/14 citations in `packs/horizontal/workflow-bpm`
are correct.

### 2.6 ✅ CONFIRMED CURRENT — 国发〔2016〕51号

《政务信息资源共享管理暂行办法》 shows no repeal, and remains the basis cited
by later instruments. The Articles 8/9/10/13/14 citations in
`packs/government-public/data-exchange` stand.

**Citation improvement:** the repository cites the CAC mirror
(`cac.gov.cn/2016-09/21/...`). Two authoritative alternatives were verified and
one is now used instead:

- 国务院公报 — <https://www.gov.cn/gongbao/content/2016/content_5115838.htm>
- 中国政府网 — <https://www.gov.cn/zhengce/content/2016-09/19/content_5109486.htm>

### 2.7 ⚠️ SECTOR RULE CHANGED — healthcare

**国卫规划发〔2026〕6号《医疗卫生机构数据安全和个人信息保护管理办法（试行）》**,
issued 2026-02-14 by five ministries, effective on promulgation, supersedes the
regulatory picture previously assumed by `packs/healthcare/his-emr`. Handled in
PR #16; listed here because it is the kind of change this audit exists to find.

## 3. What this audit did **not** cover

Stated so the scope of this document is not over-read:

- International instruments (GDPR, HIPAA, CCPA, EU AI Act, ISO/IEC, NIST,
  PCI DSS, and the technical standards). Not re-verified.
- National clinical-adaptation and local implementation rules.
- **Article-level content** of every instrument — only *currency and numbering*
  were audited, plus the specific articles this repository already quotes.
- Whether a standard's **content** matches how the packs describe it, as
  opposed to whether the standard exists and is current.

## 4. Standing guidance

1. **Never cite a CN law article number without checking whether the law has
   been amended and renumbered.** 《网络安全法》proved this within nine months of
   the packs being drafted.
2. **Prefer citing the instrument's identity (name + 文号 + version) over its
   article number** where the article adds little, and check the numbering when
   it does add a lot.
3. **A URL that returns 200 is not a verification.** The standards search
   platform returns 200 for non-existent numbers; anti-bot 403/412 responses
   (iso.org, nhc.gov.cn) likewise prove neither existence nor absence. Verify
   existence from a source that *names* the standard and its status.
4. Record unretrieved sources as unretrieved. Three sources in this repository
   remain deliberately unquoted for exactly this reason.

## 5. Reproducing this audit

The extraction is re-runnable:

```powershell
# distinct regulatory ids across manifests
Get-ChildItem -Recurse -Filter manifest.yaml | ForEach-Object {
  $in = $false
  Get-Content $_.FullName -Encoding UTF8 | ForEach-Object {
    if ($_ -match '^regulatory:') { $in = $true; return }
    if ($in -and $_ -match '^\S') { $in = $false }
    if ($in -and $_ -match 'id:\s*(\S+)') { $matches[1] }
  }
} | Sort-Object -Unique

# every article-level citation in the repository
Get-ChildItem -Recurse -Include *.md -File |
  Where-Object { $_.FullName -notmatch '\\\.git\\|_site' } |
  Select-String -Pattern '法》第[一二三四五六七八九十百零]+条' -Encoding UTF8
```

The second command currently returns **4 hits**, in
`workflow-bpm/00-context/regulatory-landscape.md` and
`data-exchange/00-context/industry-brief.md`. That is the number to watch: it
should not grow without a currency check.
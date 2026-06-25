/**
 * Generation d'un rapport PDF professionnel (type document client) via jsPDF.
 * Reprend les 5 sections du cahier des charges (3.6). Palette bleu cyber.
 */
import jsPDF from 'jspdf'
import { autoTable } from 'jspdf-autotable'
import { labelTypeActif, labelCriticite } from '@/constants/enums'

const PRIMARY = [2, 132, 199]  
const ACCENT = [14, 165, 233]   
const DARK = [15, 23, 42]
const GREY = [100, 116, 139]
const LIGHT = [241, 245, 249]
const NIVEAU = { FAIBLE: [34, 197, 94], MOYEN: [234, 179, 8], ELEVE: [239, 68, 68] }

export function genererRapportPdf(rapport) {
  const doc = new jsPDF({ unit: 'pt', format: 'a4' })
  const W = doc.internal.pageSize.getWidth()
  const e = rapport.entreprise
  const niveau = rapport.analyse_risque.niveau_risque
  const dateStr = new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' })

  doc.setFillColor(...PRIMARY)
  doc.rect(0, 0, W, 96, 'F')

  doc.setFillColor(255, 255, 255)
  doc.setDrawColor(255, 255, 255)
  drawShield(doc, 44, 34, 26)
  doc.setTextColor(255)
  doc.setFont('helvetica', 'bold'); doc.setFontSize(22)
  doc.text('CyberTwin', 84, 44)
  doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5)
  doc.text("Rapport d'analyse de risque cyber", 84, 62)
  doc.setFontSize(9.5)
  doc.text(`Genere le ${dateStr}`, W - 40, 40, { align: 'right' })
  doc.text(`Reference : CT-${String(e.id).padStart(4, '0')}-${new Date().getFullYear()}`, W - 40, 56, { align: 'right' })
  doc.text('Document confidentiel', W - 40, 72, { align: 'right' })
  doc.setFillColor(...ACCENT)
  doc.rect(0, 96, W, 4, 'F')

  let y = 124
  doc.setFillColor(...LIGHT)
  doc.roundedRect(40, y, W - 80, 78, 8, 8, 'F')
  doc.setTextColor(...DARK); doc.setFont('helvetica', 'bold'); doc.setFontSize(15)
  doc.text(e.nom, 58, y + 28)
  doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(...GREY)
  doc.text(`Secteur : ${e.secteur_activite}`, 58, y + 46)
  doc.text(`${e.nombre_employes} employes  -  ${rapport.inventaire_actifs.length} actifs  -  ${rapport.vulnerabilites_detectees.length} vulnerabilites`, 58, y + 62)

  const col = NIVEAU[niveau] || GREY
  doc.setFillColor(...col)
  doc.roundedRect(W - 196, y + 16, 138, 46, 6, 6, 'F')
  doc.setTextColor(255); doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5)
  doc.text('NIVEAU DE RISQUE', W - 127, y + 32, { align: 'center' })
  doc.setFont('helvetica', 'bold'); doc.setFontSize(16)
  doc.text(niveau, W - 127, y + 50, { align: 'center' })
  y += 78 + 28

  y = sectionTitre(doc, '1. Presentation de l\'entreprise', y)
  autoTable(doc, {
    startY: y,
    theme: 'grid',
    body: [
      ['Nom', e.nom, 'Secteur', e.secteur_activite],
      ['Employes', String(e.nombre_employes), 'Serveurs', String(e.nombre_serveurs)],
      ['Postes clients', String(e.nombre_postes_clients), 'Services exposes', (e.services_exposes || []).join(', ') || 'Aucun'],
    ],
    styles: { fontSize: 9.5, cellPadding: 6, lineColor: [226, 232, 240], textColor: DARK },
    columnStyles: {
      0: { fontStyle: 'bold', fillColor: LIGHT, textColor: GREY, cellWidth: 92 },
      2: { fontStyle: 'bold', fillColor: LIGHT, textColor: GREY, cellWidth: 92 },
    },
    margin: { left: 40, right: 40 },
  })
  y = doc.lastAutoTable.finalY + 26

  y = sectionTitre(doc, `2. Inventaire des actifs (${rapport.inventaire_actifs.length})`, y)
  autoTable(doc, {
    startY: y,
    head: [['Nom', 'Type', 'Description']],
    body: rapport.inventaire_actifs.map((a) => [a.nom, labelTypeActif(a.type_actif), a.description || '-']),
    headStyles: { fillColor: PRIMARY, textColor: 255, fontSize: 9.5 },
    alternateRowStyles: { fillColor: [248, 250, 252] },
    styles: { fontSize: 9, cellPadding: 5, textColor: DARK },
    margin: { left: 40, right: 40 },
  })
  y = doc.lastAutoTable.finalY + 26

  if (y > 660) { doc.addPage(); y = 60 }
  y = sectionTitre(doc, `3. Vulnerabilites detectees (${rapport.vulnerabilites_detectees.length})`, y)
  autoTable(doc, {
    startY: y,
    head: [['Libelle', 'Criticite', 'Description']],
    body: rapport.vulnerabilites_detectees.map((v) => [v.libelle, labelCriticite(v.criticite), v.description || '-']),
    headStyles: { fillColor: PRIMARY, textColor: 255, fontSize: 9.5 },
    alternateRowStyles: { fillColor: [248, 250, 252] },
    styles: { fontSize: 9, cellPadding: 5, textColor: DARK },
    columnStyles: { 1: { cellWidth: 80 } },
    margin: { left: 40, right: 40 },
    didParseCell: (d) => {
      if (d.section === 'body' && d.column.index === 1) {
        const map = { Faible: [34, 197, 94], Moyenne: [234, 179, 8], Elevee: [249, 115, 22], Critique: [239, 68, 68] }
        const c = map[d.cell.raw]
        if (c) { d.cell.styles.textColor = c; d.cell.styles.fontStyle = 'bold' }
      }
    },
  })
  y = doc.lastAutoTable.finalY + 26

  if (y > 700) { doc.addPage(); y = 60 }
  y = sectionTitre(doc, '4. Niveau de risque', y)
  doc.setFillColor(...col)
  doc.roundedRect(40, y, W - 80, 56, 6, 6, 'F')
  doc.setTextColor(255); doc.setFont('helvetica', 'bold'); doc.setFontSize(13)
  doc.text(`Niveau : ${niveau}`, 58, y + 24)
  doc.setFont('helvetica', 'normal'); doc.setFontSize(11)
  doc.text(`Score global : ${rapport.analyse_risque.score}`, 58, y + 42)
  const d = rapport.analyse_risque.details || {}
  doc.setFontSize(9)
  doc.text(`Detail : vulnerabilites ${d.score_vulnerabilites ?? '-'}  |  exposition ${d.score_exposition ?? '-'}  |  actifs ${d.score_actifs ?? '-'}`, W - 58, y + 33, { align: 'right' })
  y += 56 + 26

  if (y > 720) { doc.addPage(); y = 60 }
  y = sectionTitre(doc, '5. Recommandations de securite', y)
  doc.setFontSize(10); doc.setFont('helvetica', 'normal')
  rapport.recommandations.forEach((r) => {
    if (y > 790) { doc.addPage(); y = 60 }
    doc.setFillColor(...ACCENT); doc.circle(47, y - 3, 2.2, 'F')
    doc.setTextColor(...DARK)
    const lignes = doc.splitTextToSize(r, W - 120)
    doc.text(lignes, 58, y)
    y += lignes.length * 14 + 7
  })

  const total = doc.internal.getNumberOfPages()
  for (let i = 1; i <= total; i++) {
    doc.setPage(i)
    doc.setDrawColor(...LIGHT); doc.setLineWidth(0.8)
    doc.line(40, 812, W - 40, 812)
    doc.setTextColor(...GREY); doc.setFontSize(8)
    doc.text('CyberTwin - Sentinea  |  Document confidentiel', 40, 826)
    doc.text(`Page ${i} / ${total}`, W - 40, 826, { align: 'right' })
  }

  doc.save(`rapport-cybertwin-${e.nom.replace(/\s+/g, '-').toLowerCase()}.pdf`)
}

function sectionTitre(doc, texte, y) {
  doc.setTextColor(...PRIMARY); doc.setFont('helvetica', 'bold'); doc.setFontSize(13)
  doc.text(texte, 40, y)
  doc.setDrawColor(...ACCENT); doc.setLineWidth(2)
  doc.line(40, y + 6, 64, y + 6)
  return y + 22
}

function drawShield(doc, cx, cy, s) {
  const x = cx, y = cy
  doc.setFillColor(255, 255, 255)
  doc.triangle(x - s * 0.5, y - s * 0.4, x + s * 0.5, y - s * 0.4, x, y - s * 0.4, 'F')

  doc.setLineWidth(0)
  const pts = [
    [x, y - s * 0.55], [x + s * 0.5, y - s * 0.35], [x + s * 0.5, y + s * 0.1],
    [x, y + s * 0.55], [x - s * 0.5, y + s * 0.1], [x - s * 0.5, y - s * 0.35],
  ]
  doc.setFillColor(255, 255, 255)
  doc.lines(
    pts.slice(1).map((p, i) => [p[0] - pts[i][0], p[1] - pts[i][1]]),
    pts[0][0], pts[0][1], [1, 1], 'F', true,
  )

  doc.setDrawColor(...PRIMARY); doc.setLineWidth(2)
  doc.line(x - s * 0.22, y, x - s * 0.05, y + s * 0.18)
  doc.line(x - s * 0.05, y + s * 0.18, x + s * 0.25, y - s * 0.2)
}

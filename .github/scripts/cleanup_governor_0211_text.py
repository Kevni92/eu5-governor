from pathlib import Path

ROOT = Path('.')

def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8-sig')

def replace(text, old, new):
    return text.replace(old, new)

# German: avoid awkward 'Nicht-Kron-Gouverneur' and misleading 'freiwillige Entlassung'.
p = 'main_menu/localization/german/zz_eu5gov_l_german.yml'
t = read(p)
t = replace(t,
    'Das Ersetzen des bisherigen Amtsinhabers zählt als freiwillige Entlassung und verursacht daher dessen nach Verankerung skalierende politische Kosten, sofern er nicht dem Kronstand angehört.',
    'Das Ersetzen des bisherigen Amtsinhabers verursacht dieselben nach Verankerung skalierenden politischen Kosten wie eine Entlassung, sofern er nicht dem Kronstand angehört.'
)
t = replace(t,
    'Entfernt einen Gouverneur aus seinem Amt. Bei Nicht-Kron-Gouverneuren betragen die politischen Kosten mindestens #R -10 Standeszufriedenheit#! und #R -5 Stabilität#!. Oberhalb von 10 Verankerung skalieren sie linear: 50 Verankerung kosten -50 Zufriedenheit und -25 Stabilität; 100 Verankerung kosten -100 Zufriedenheit und -50 Stabilität. Kron-Gouverneure können kostenlos entlassen werden.',
    'Entfernt einen Gouverneur aus seinem Amt. Gehört er einem anderen Stand als dem Kronstand an, betragen die politischen Kosten mindestens #R -10 Standeszufriedenheit#! und #R -5 Stabilität#!. Oberhalb von 10 Verankerung skalieren sie linear: 50 Verankerung kosten -50 Zufriedenheit und -25 Stabilität; 100 Verankerung kosten -100 Zufriedenheit und -50 Stabilität. Für Gouverneure des Kronstands entfallen diese Kosten.'
)
t = replace(t,
    'Die Entlassung oder Ersetzung eines Nicht-Kron-Gouverneurs kostet mindestens -10 Standeszufriedenheit / -5 Stabilität und skaliert danach mit der Verankerung bis -100 / -50 bei 100. Kron-Gouverneure sind davon ausgenommen.',
    'Gehört der Gouverneur einem anderen Stand als dem Kronstand an, kostet seine Entlassung oder Ersetzung mindestens -10 Standeszufriedenheit / -5 Stabilität und skaliert danach mit der Verankerung bis -100 / -50 bei 100. Für Gouverneure des Kronstands entfallen diese Kosten.'
)
write(p, t)

# English: same conceptual cleanup, without shorthand 'non-Crown Governor'.
p = 'main_menu/localization/english/zz_eu5gov_l_english.yml'
t = read(p)
t = replace(t,
    'Replacing the current office holder counts as a voluntary dismissal and therefore pays the outgoing Governor\'s Entrenchment-scaled political cost unless they belong to the Crown Estate.',
    'Replacing the current office holder applies the same Entrenchment-scaled political cost as dismissal unless the outgoing Governor belongs to the Crown Estate.'
)
t = replace(t,
    'Remove a Governor from office. Non-Crown Governors always cost at least #R -10 Estate Satisfaction#! and #R -5 Stability#!. Above 10 Entrenchment the cost scales linearly: 50 Entrenchment costs -50 Satisfaction and -25 Stability; 100 Entrenchment costs -100 Satisfaction and -50 Stability. Crown Governors are free to dismiss.',
    'Remove a Governor from office. If they belong to an Estate other than the Crown Estate, dismissal costs at least #R -10 Estate Satisfaction#! and #R -5 Stability#!. Above 10 Entrenchment the cost scales linearly: 50 Entrenchment costs -50 Satisfaction and -25 Stability; 100 Entrenchment costs -100 Satisfaction and -50 Stability. Crown Estate Governors do not pay these costs.'
)
t = replace(t,
    'Voluntary dismissal or replacement of a non-Crown Governor costs at least -10 Estate Satisfaction / -5 Stability and otherwise scales with Entrenchment up to -100 / -50 at 100. Crown Governors are exempt.',
    'If the Governor belongs to an Estate other than the Crown Estate, dismissal or replacement costs at least -10 Estate Satisfaction / -5 Stability and otherwise scales with Entrenchment up to -100 / -50 at 100. Crown Estate Governors do not pay these costs.'
)
write(p, t)

# Comments only, but keep terminology aligned with the player-facing rules.
p = 'in_game/common/scripted_effects/eu5gov_governor_effects.txt'
t = read(p)
t = replace(t,
    '# Voluntary dismissal/replacement is free for Crown characters. Otherwise the',
    '# Dismissal/replacement is free for Crown Estate characters. Otherwise the'
)
write(p, t)

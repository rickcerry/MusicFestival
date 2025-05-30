from . import dbDays
from . import dbTicketTypes
from . import dbStages

# Populate and initialize the database (according to Exam text)
def run():
          dbDays.clearDays()
          dbStages.clearStages()
          dbTicketTypes.clearTicketTypes()
          
          print("Starting intialization: DAYS")
          dbDays.insertDay("Venerdì", "2025-07-18")
          dbDays.insertDay("Sabato", "2025-07-19")
          dbDays.insertDay("Domenica", "2025-07-20")
          
          print("Starting initialization: STAGES")
          dbStages.insertStage("Palco A", "Main Stage")
          dbStages.insertStage("Palco B", "Secondary Stage")
          dbStages.insertStage("Palco C", "Experimental Stage")
          
          print("Starting initialization: TICKET TYPES")
          dbTicketTypes.insertTicketType("Biglietto Giornaliero", 1, "-Consente l’ingresso al festival per una singola giornata a scelta.-Ideale per chi vuole vivere l’esperienza in modo concentrato o seguire un artista specifico.", "35.00")
          dbTicketTypes.insertTicketType("Pass 2 Giorni", 2, "-Permette l’accesso al festival per due giornate consecutive.-Una soluzione conveniente per chi desidera godersi buona parte della manifestazione, con un risparmio di €10 rispetto all’acquisto di due biglietti giornalieri.", "60.00")
          dbTicketTypes.insertTicketType("Full Pass", 3, "-Garantisce l’ingresso per l’intera durata del festival.-La scelta migliore per vivere ogni momento senza limiti, con un risparmio di €25 rispetto all’acquisto di tre biglietti giornalieri.", "80.00")
          
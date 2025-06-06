from . import dbDays
from . import dbTicketTypes
from . import dbStages
from . import dbTickets
from . import dbUsers
from . import dbPerformances

# Populate and initialize the database (according to Exam text)
def run():
          dbDays.clearDays()
          dbStages.clearStages()
          dbTicketTypes.clearTicketTypes()
          dbTickets.clearTickets()
          dbUsers.clearUsers()
          dbPerformances.clearPerformances()
          
          print("Starting intialization: DAYS")
          dbDays.insertDay("Venerdì", "2025-07-18", 0)
          dbDays.insertDay("Sabato", "2025-07-19", 0)
          dbDays.insertDay("Domenica", "2025-07-20", 0)
          
          print("Starting initialization: STAGES")
          dbStages.insertStage("Palco A", "Main Stage")
          dbStages.insertStage("Palco B", "Secondary Stage")
          dbStages.insertStage("Palco C", "Experimental Stage")
          
          print("Starting initialization: TICKET TYPES")
          dbTicketTypes.insertTicketType("Biglietto Giornaliero", 1, '<li>Consente l’ingresso al festival per una singola giornata a scelta.</li><li>Ideale per chi vuole vivere l’esperienza in modo concentrato o seguire un artista specifico.</li>', "35.00")
          dbTicketTypes.insertTicketType("Pass 2 Giorni", 2, '<li>Permette l’accesso al festival per due giornate consecutive.</li><li>Una soluzione conveniente per chi desidera godersi buona parte della manifestazione, con un risparmio di €10 rispetto all’acquisto di due biglietti giornalieri.</li>', "60.00")
          dbTicketTypes.insertTicketType("Full Pass", 3, '<li>Garantisce l’ingresso per l’intera durata del festival.</li><li>La scelta migliore per vivere ogni momento senza limiti, con un risparmio di €25 rispetto all’acquisto di tre biglietti giornalieri.</li>', "80.00")
          
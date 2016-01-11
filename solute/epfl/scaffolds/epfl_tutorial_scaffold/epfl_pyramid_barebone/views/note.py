from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView

from first_step import NoteModel
from first_step import NoteLayout


class NoteRoot(NoteLayout):

    def init_struct(self):
        note_id = self.page.request.matchdict.get(
            'note_id', None)

        try:
            note_data = self.page.model.get_note(int(note_id))
        except:
            self.page.show_fading_message('No data available', 'error')
            return

        self.node_list.extend(
            [components.Box(cid='note_display',
                            title='View note',
                            node_list=[
                                components.Text(tag='h3',
                                                verbose=True,
                                                value=note_data['title']),
                                components.Text(value=note_data['text'])])
             ]
        )


@EPFLView(route_name='Note', route_pattern='/note/{note_id}')
class NotePage(epfl.Page):

    root_node = NoteRoot()
    model = NoteModel

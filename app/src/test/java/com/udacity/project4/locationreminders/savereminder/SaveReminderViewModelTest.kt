package com.udacity.project4.locationreminders.savereminder

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.udacity.project4.R
import com.udacity.project4.locationreminders.data.FakeDataSource
import com.udacity.project4.locationreminders.reminderslist.ReminderDataItem
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.TestCoroutineDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.mockito.Mockito.`when`
import org.mockito.Mockito.mock

@ExperimentalCoroutinesApi
class SaveReminderViewModelTest {
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private val testDispatcher = TestCoroutineDispatcher()
    private lateinit var dataSource: FakeDataSource
    private lateinit var viewModel: SaveReminderViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        dataSource = FakeDataSource()
        val app = mock(Application::class.java)
        `when`(app.getString(R.string.reminder_saved)).thenReturn("Reminder Saved !")
        viewModel = SaveReminderViewModel(
            app,
            dataSource
        )
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
        testDispatcher.cleanupTestCoroutines()
    }

    @Test
    fun validateAndSaveReminder_validReminder_savesAndShowsToast() {
        val reminder = ReminderDataItem("Title", "Description", "Location", 1.0, 2.0, "id-1")

        viewModel.validateAndSaveReminder(reminder)

        assertThat(viewModel.showToast.value, `is`("Reminder Saved !"))
        assertThat(viewModel.showLoading.value, `is`(false))
    }

    @Test
    fun validateAndSaveReminder_missingTitle_showsTitleError() {
        val reminder = ReminderDataItem(null, "Description", "Location", 1.0, 2.0, "id-1")

        viewModel.validateAndSaveReminder(reminder)

        assertThat(viewModel.showSnackBarInt.value, `is`(R.string.err_enter_title))
    }

    @Test
    fun validateAndSaveReminder_missingLocation_showsLocationError() {
        val reminder = ReminderDataItem("Title", "Description", null, 1.0, 2.0, "id-1")

        viewModel.validateAndSaveReminder(reminder)

        assertThat(viewModel.showSnackBarInt.value, `is`(R.string.err_select_location))
    }
}
